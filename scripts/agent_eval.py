#!/usr/bin/env python3
"""Prepare and score paired with/without-skill structural agent evals."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gtta.discipline import SUPPORTED_EVIDENCE_MODES, check_contract  # noqa: E402


BENCHMARK_VERSION = "gtta-agent-eval@1.0.0"
DEFAULT_CASES = ROOT / "evals" / "agent-eval" / "benchmark-cases.jsonl"
BASELINE_INSTRUCTIONS = """You are a strategic-risk analyst. Answer the user directly, distinguish uncertainty from known information, and give decision-useful analysis. Do not claim to have checked sources that you did not access."""
REQUIRED_CASE_FIELDS = {
    "id",
    "title",
    "mode",
    "evidence_mode",
    "prompt",
    "context",
}


class EvalInputError(ValueError):
    """Raised when benchmark input is incomplete or inconsistent."""


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise EvalInputError(
                    f"{path}:{line_number}: invalid JSON: {exc.msg}"
                ) from exc
            if not isinstance(row, dict):
                raise EvalInputError(f"{path}:{line_number}: expected a JSON object")
            rows.append(row)
    return rows


def load_cases(path: Path) -> list[dict[str, Any]]:
    """Load and validate a 10-20 case structural comparison suite."""
    if not path.is_file():
        raise EvalInputError(f"case file does not exist: {path}")
    cases = _read_jsonl(path)
    if not 10 <= len(cases) <= 20:
        raise EvalInputError("benchmark suite must contain between 10 and 20 cases")

    seen: set[str] = set()
    for index, case in enumerate(cases, start=1):
        missing = REQUIRED_CASE_FIELDS - case.keys()
        extra = case.keys() - REQUIRED_CASE_FIELDS
        if missing or extra:
            raise EvalInputError(
                f"case {index}: fields mismatch; missing={sorted(missing)}, "
                f"extra={sorted(extra)}"
            )
        case_id = case["id"]
        if not isinstance(case_id, str) or not case_id.strip():
            raise EvalInputError(f"case {index}: id must be a non-empty string")
        if case_id in seen:
            raise EvalInputError(f"duplicate case id: {case_id}")
        seen.add(case_id)
        if case["mode"] not in tuple("ABCDEFG"):
            raise EvalInputError(f"{case_id}: mode must be A-G")
        if case["evidence_mode"] not in SUPPORTED_EVIDENCE_MODES:
            raise EvalInputError(f"{case_id}: unsupported evidence mode")
        for field in ("title", "prompt", "context"):
            if not isinstance(case[field], str) or not case[field].strip():
                raise EvalInputError(f"{case_id}: {field} must be non-empty text")
    return cases


def _sample_id(seed: int, case_id: str, arm: str) -> str:
    material = f"{BENCHMARK_VERSION}|{seed}|{case_id}|{arm}".encode()
    return hashlib.sha256(material).hexdigest()[:16]


def _user_message(case: dict[str, Any]) -> str:
    return (
        f"Decision task: {case['prompt']}\n\n"
        f"Context: {case['context']}\n\n"
        f"Requested output: Mode {case['mode']} memo.\n"
        f"Evidence mode: {case['evidence_mode']}."
    )


def prepare_run(case_path: Path, output_dir: Path, seed: int) -> dict[str, Any]:
    """Create opaque paired requests and a private arm mapping."""
    cases = load_cases(case_path)
    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    skill_hash = hashlib.sha256(skill_text.encode()).hexdigest()

    try:
        output_dir.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise EvalInputError(f"output directory already exists: {output_dir}") from exc

    requests: list[dict[str, Any]] = []
    samples: list[dict[str, Any]] = []
    for case in cases:
        for arm in ("baseline", "skill"):
            sample_id = _sample_id(seed, case["id"], arm)
            system = BASELINE_INSTRUCTIONS
            if arm == "skill":
                system += (
                    "\n\nApply the following Global Think Tank Analyst runtime "
                    f"method exactly:\n\n<gtta-skill>\n{skill_text}\n</gtta-skill>"
                )
            requests.append(
                {
                    "sample_id": sample_id,
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": _user_message(case)},
                    ],
                }
            )
            samples.append(
                {
                    "sample_id": sample_id,
                    "case_id": case["id"],
                    "arm": arm,
                    "mode": case["mode"],
                    "evidence_mode": case["evidence_mode"],
                }
            )

    random.Random(seed).shuffle(requests)
    request_text = "\n".join(
        json.dumps(row, ensure_ascii=False) for row in requests
    )
    (output_dir / "requests.jsonl").write_text(request_text + "\n", encoding="utf-8")
    mapping = {
        "benchmark_version": BENCHMARK_VERSION,
        "seed": seed,
        "case_count": len(cases),
        "sample_count": len(samples),
        "skill_sha256": skill_hash,
        "samples": samples,
    }
    (output_dir / "private-mapping.json").write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "outputs.template.jsonl").write_text(
        "\n".join(
            json.dumps({"sample_id": row["sample_id"], "output": ""})
            for row in requests
        )
        + "\n",
        encoding="utf-8",
    )
    return mapping


def score_run(run_dir: Path, output_path: Path) -> dict[str, Any]:
    """Score observable contract findings without claiming content quality."""
    mapping_path = run_dir / "private-mapping.json"
    if not mapping_path.is_file():
        raise EvalInputError(f"run mapping does not exist: {mapping_path}")
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    samples = {row["sample_id"]: row for row in mapping["samples"]}

    output_rows = _read_jsonl(output_path)
    outputs: dict[str, str] = {}
    for row in output_rows:
        if set(row) != {"sample_id", "output"}:
            raise EvalInputError("each output row must contain sample_id and output")
        sample_id = row["sample_id"]
        if sample_id not in samples:
            raise EvalInputError(f"unknown sample id: {sample_id}")
        if sample_id in outputs:
            raise EvalInputError(f"duplicate output for sample id: {sample_id}")
        if not isinstance(row["output"], str) or not row["output"].strip():
            raise EvalInputError(f"empty output for sample id: {sample_id}")
        outputs[sample_id] = row["output"]
    missing = samples.keys() - outputs.keys()
    if missing:
        raise EvalInputError(f"missing outputs for {len(missing)} sample(s)")

    detail: list[dict[str, Any]] = []
    aggregates: dict[str, dict[str, Any]] = {}
    for arm in ("baseline", "skill"):
        aggregates[arm] = {
            "samples": 0,
            "passed": 0,
            "error_findings": 0,
            "warning_findings": 0,
            "rule_counts": Counter(),
        }

    for sample_id, sample in samples.items():
        report = check_contract(outputs[sample_id], mode=sample["mode"])
        findings = [finding.to_dict() for finding in report.findings]
        evidence_mode_matches = report.evidence_mode == sample["evidence_mode"]
        if not evidence_mode_matches:
            findings.append(
                {
                    "rule_id": "GTTAE001",
                    "severity": "error",
                    "message": (
                        "Declared evidence mode does not match the benchmark "
                        f"case: expected {sample['evidence_mode']!r}, got "
                        f"{report.evidence_mode!r}."
                    ),
                }
            )
        sample_passed = report.passed and evidence_mode_matches
        detail.append(
            {
                "sample_id": sample_id,
                "case_id": sample["case_id"],
                "arm": sample["arm"],
                "passed": sample_passed,
                "findings": findings,
            }
        )
        aggregate = aggregates[sample["arm"]]
        aggregate["samples"] += 1
        aggregate["passed"] += int(sample_passed)
        for finding in findings:
            aggregate[f"{finding['severity']}_findings"] += 1
            aggregate["rule_counts"][finding["rule_id"]] += 1

    for aggregate in aggregates.values():
        aggregate["rule_counts"] = dict(sorted(aggregate["rule_counts"].items()))
        aggregate["pass_rate"] = aggregate["passed"] / aggregate["samples"]

    return {
        "benchmark_version": mapping["benchmark_version"],
        "ruleset_version": check_contract("", mode=None).ruleset_version,
        "scope": "deterministic-method-contract-only",
        "aggregates": aggregates,
        "samples": sorted(detail, key=lambda row: (row["case_id"], row["arm"])),
        "limitations": [
            "This report does not score factuality, source support, or decision quality.",
            "A same-model or author-run comparison is a structural sanity check, not external validation.",
            "External practitioner validation remains a separate unmet evidence layer.",
        ],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate benchmark cases")
    validate.add_argument("--cases", type=Path, default=DEFAULT_CASES)

    prepare = subparsers.add_parser("prepare", help="prepare paired requests")
    prepare.add_argument("output_dir", type=Path)
    prepare.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    prepare.add_argument("--seed", type=int, default=20260830)

    score = subparsers.add_parser("score", help="score a completed paired run")
    score.add_argument("run_dir", type=Path)
    score.add_argument("outputs", type=Path)
    score.add_argument("--report", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "validate":
            cases = load_cases(args.cases)
            print(f"OK: {len(cases)} benchmark cases")
            return 0
        if args.command == "prepare":
            mapping = prepare_run(args.cases, args.output_dir, args.seed)
            print(
                f"OK: prepared {mapping['sample_count']} samples from "
                f"{mapping['case_count']} cases in {args.output_dir}"
            )
            return 0
        report = score_run(args.run_dir, args.outputs)
        serialized = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.report:
            args.report.write_text(serialized, encoding="utf-8")
        print(serialized, end="")
        return 0
    except (EvalInputError, OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
