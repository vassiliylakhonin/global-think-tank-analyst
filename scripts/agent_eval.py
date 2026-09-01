#!/usr/bin/env python3
"""Prepare and score paired with/without-skill structural agent evals."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gtta.discipline import (  # noqa: E402
    FINDING_LIMITS,
    SUPPORTED_EVIDENCE_MODES,
    check_contract,
)


BENCHMARK_VERSION = "gtta-agent-eval@1.1.0"
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
DEFAULT_MAX_SEQUENCE_SIMILARITY = 0.90
DEFAULT_MAX_SHARED_LINE_RATIO = 0.80


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


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(64 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_antigravity_bundle(
    output_dir: Path, requests: list[dict[str, Any]]
) -> None:
    """Write provider-neutral Markdown tasks for manual Antigravity execution."""
    task_dir = output_dir / "antigravity-tasks"
    response_dir = output_dir / "antigravity-responses"
    task_dir.mkdir()
    response_dir.mkdir()

    manifest: list[dict[str, str]] = []
    for position, request in enumerate(requests, start=1):
        sample_id = request["sample_id"]
        filename = f"{position:02d}-{sample_id}.md"
        messages = request["messages"]
        task = f"""# GTTA paired-eval sample `{sample_id}`

Run this sample in a fresh Antigravity conversation. Keep the same model and
generation settings for every sample. Do not add instructions beyond the two
messages below. Save only the model's final response as
`../antigravity-responses/{sample_id}.md`.

## System message

<system>
{messages[0]["content"]}
</system>

## User message

<user>
{messages[1]["content"]}
</user>
"""
        (task_dir / filename).write_text(task, encoding="utf-8")
        manifest.append({"sample_id": sample_id, "task_file": filename})

    (output_dir / "antigravity-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    metadata_template = {
        "runner": "Antigravity",
        "app_version": "",
        "model": "",
        "generation_settings": {},
        "notes": "",
    }
    (output_dir / "run-metadata.template.json").write_text(
        json.dumps(metadata_template, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (task_dir / "README.md").write_text(
        """# Antigravity run instructions

1. Fill `../run-metadata.template.json` before generation.
2. Use one fresh conversation per numbered task.
3. Use exactly the same model and generation settings for all tasks.
4. Save only each final response to the filename stated in its task.
5. Do not inspect `../private-mapping.json` until all responses are saved.
6. Run `agent_eval.py import-antigravity`, then `agent_eval.py score`.

The harness performs no API or network calls.
""",
        encoding="utf-8",
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
    _write_antigravity_bundle(output_dir, requests)
    return mapping


def import_antigravity_responses(
    run_dir: Path,
    response_dir: Path,
    metadata_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    """Import one Markdown response per opaque sample without model API calls."""
    mapping_path = run_dir / "private-mapping.json"
    requests_path = run_dir / "requests.jsonl"
    recorded_metadata_path = run_dir / "run-metadata.json"
    if not mapping_path.is_file() or not requests_path.is_file():
        raise EvalInputError("run directory is missing prepare output")
    if output_path.absolute() == recorded_metadata_path.absolute():
        raise EvalInputError("output path must not overwrite run-metadata.json")
    if output_path.exists():
        raise EvalInputError(f"output path already exists: {output_path}")
    if recorded_metadata_path.exists():
        raise EvalInputError(
            f"recorded run metadata already exists: {recorded_metadata_path}"
        )
    if not response_dir.is_dir():
        raise EvalInputError(f"response directory does not exist: {response_dir}")

    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    requests = _read_jsonl(requests_path)
    expected_ids = {sample["sample_id"] for sample in mapping["samples"]}
    request_ids = [request["sample_id"] for request in requests]
    if set(request_ids) != expected_ids:
        raise EvalInputError("request IDs do not match the private mapping")

    response_files = {
        path.stem: path
        for path in response_dir.glob("*.md")
        if not path.name.startswith(".")
    }
    missing = expected_ids - response_files.keys()
    unknown = response_files.keys() - expected_ids
    if missing or unknown:
        raise EvalInputError(
            "response files mismatch; "
            f"missing={len(missing)}, unknown={sorted(unknown)}"
        )

    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    required_metadata = {
        "runner",
        "app_version",
        "model",
        "generation_settings",
        "notes",
    }
    if set(metadata) != required_metadata:
        raise EvalInputError(
            "run metadata fields mismatch; expected "
            + ", ".join(sorted(required_metadata))
        )
    for field in ("runner", "app_version", "model"):
        if not isinstance(metadata[field], str) or not metadata[field].strip():
            raise EvalInputError(f"run metadata {field} must be non-empty")
    if not isinstance(metadata["generation_settings"], dict):
        raise EvalInputError("run metadata generation_settings must be an object")
    if not isinstance(metadata["notes"], str):
        raise EvalInputError("run metadata notes must be text")

    output_rows: list[dict[str, str]] = []
    for sample_id in request_ids:
        response = response_files[sample_id].read_text(encoding="utf-8").strip()
        if not response:
            raise EvalInputError(f"empty response for sample id: {sample_id}")
        output_rows.append({"sample_id": sample_id, "output": response})
    output_path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in output_rows) + "\n",
        encoding="utf-8",
    )

    recorded_metadata = {
        **metadata,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "sample_count": len(output_rows),
        "requests_sha256": _sha256_file(requests_path),
        "outputs_sha256": _sha256_file(output_path),
    }
    recorded_metadata_path.write_text(
        json.dumps(recorded_metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return recorded_metadata


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
            "truncated_samples": 0,
            "truncated_rule_counts": Counter(),
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
                "findings_truncated": bool(report.truncated_rule_ids),
                "truncated_rule_ids": list(report.truncated_rule_ids),
            }
        )
        aggregate = aggregates[sample["arm"]]
        aggregate["samples"] += 1
        aggregate["passed"] += int(sample_passed)
        aggregate["truncated_samples"] += int(bool(report.truncated_rule_ids))
        for rule_id in report.truncated_rule_ids:
            aggregate["truncated_rule_counts"][rule_id] += 1
        for finding in findings:
            aggregate[f"{finding['severity']}_findings"] += 1
            aggregate["rule_counts"][finding["rule_id"]] += 1

    for aggregate in aggregates.values():
        aggregate["rule_counts"] = dict(sorted(aggregate["rule_counts"].items()))
        aggregate["truncated_rule_counts"] = dict(
            sorted(aggregate["truncated_rule_counts"].items())
        )
        aggregate["pass_rate"] = aggregate["passed"] / aggregate["samples"]

    findings_truncated = any(
        aggregate["truncated_samples"] for aggregate in aggregates.values()
    )

    metadata_path = run_dir / "run-metadata.json"
    run_metadata = (
        json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata_path.is_file()
        else None
    )
    limitations = [
        "This report does not score factuality, source support, or decision quality.",
        "A same-model or author-run comparison is a structural sanity check, not external validation.",
        "External practitioner validation remains a separate unmet evidence layer.",
    ]
    if run_metadata is None:
        limitations.append(
            "Run metadata was not recorded; do not use this report for an M3 claim."
        )
    if findings_truncated:
        limitations.append(
            "One or more samples reached a configured finding limit; stored "
            "finding counts are lower bounds for those samples."
        )
    return {
        "benchmark_version": mapping["benchmark_version"],
        "ruleset_version": check_contract("", mode=None).ruleset_version,
        "scope": "deterministic-method-contract-only",
        "findings_truncated": findings_truncated,
        "finding_limits": dict(FINDING_LIMITS),
        "seed": mapping["seed"],
        "skill_sha256": mapping["skill_sha256"],
        "run_metadata": run_metadata,
        "aggregates": aggregates,
        "samples": sorted(detail, key=lambda row: (row["case_id"], row["arm"])),
        "limitations": limitations,
    }


def _outputs_by_case_arm(
    run_dir: Path, output_path: Path
) -> dict[tuple[str, str], str]:
    mapping_path = run_dir / "private-mapping.json"
    if not mapping_path.is_file():
        raise EvalInputError(f"run mapping does not exist: {mapping_path}")
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    samples = {row["sample_id"]: row for row in mapping["samples"]}
    outputs: dict[str, str] = {}
    for row in _read_jsonl(output_path):
        if set(row) != {"sample_id", "output"}:
            raise EvalInputError("each output row must contain sample_id and output")
        sample_id = row["sample_id"]
        if sample_id not in samples:
            raise EvalInputError(f"unknown sample id: {sample_id}")
        if sample_id in outputs:
            raise EvalInputError(f"duplicate output for sample id: {sample_id}")
        output = row["output"]
        if not isinstance(output, str) or not output.strip():
            raise EvalInputError(f"empty output for sample id: {sample_id}")
        outputs[sample_id] = output
    missing = samples.keys() - outputs.keys()
    if missing:
        raise EvalInputError(f"missing outputs for {len(missing)} sample(s)")
    return {
        (sample["case_id"], sample["arm"]): outputs[sample_id]
        for sample_id, sample in samples.items()
    }


def _normalized_text(text: str) -> str:
    return " ".join(text.casefold().split())


def _normalized_nonempty_lines(text: str) -> list[str]:
    return [
        " ".join(line.casefold().split())
        for line in text.splitlines()
        if line.strip()
    ]


def _similarity(candidate: str, reference: str) -> tuple[float, float]:
    sequence_similarity = SequenceMatcher(
        None,
        _normalized_text(candidate),
        _normalized_text(reference),
        autojunk=False,
    ).ratio()
    candidate_lines = _normalized_nonempty_lines(candidate)
    reference_lines = _normalized_nonempty_lines(reference)
    denominator = min(len(candidate_lines), len(reference_lines))
    if denominator == 0:
        shared_line_ratio = 0.0
    else:
        matcher = SequenceMatcher(
            None, candidate_lines, reference_lines, autojunk=False
        )
        shared_line_ratio = sum(
            block.size for block in matcher.get_matching_blocks()
        ) / denominator
    return sequence_similarity, shared_line_ratio


def verify_freshness(
    run_dir: Path,
    output_path: Path,
    references: list[tuple[Path, Path]],
    *,
    max_sequence_similarity: float = DEFAULT_MAX_SEQUENCE_SIMILARITY,
    max_shared_line_ratio: float = DEFAULT_MAX_SHARED_LINE_RATIO,
) -> dict[str, Any]:
    """Detect exact reuse and high-confidence near-copying across paired runs."""
    for label, value in (
        ("max sequence similarity", max_sequence_similarity),
        ("max shared-line ratio", max_shared_line_ratio),
    ):
        if not 0.0 <= value <= 1.0:
            raise EvalInputError(f"{label} must be between 0 and 1")

    current = _outputs_by_case_arm(run_dir, output_path)
    comparisons: list[dict[str, Any]] = []
    passed = True
    for reference_run, reference_output in references:
        reference = _outputs_by_case_arm(reference_run, reference_output)
        if current.keys() != reference.keys():
            missing = sorted(current.keys() - reference.keys())
            extra = sorted(reference.keys() - current.keys())
            raise EvalInputError(
                "candidate and reference case/arm sets differ; "
                f"missing={missing}, extra={extra}"
            )

        exact_duplicates: list[dict[str, Any]] = []
        near_duplicates: list[dict[str, Any]] = []
        max_sequence: tuple[float, str, str] = (-1.0, "", "")
        max_shared_lines: tuple[float, str, str] = (-1.0, "", "")
        for (case_id, arm), candidate in sorted(current.items()):
            prior = reference[(case_id, arm)]
            if candidate == prior:
                exact_duplicates.append({"case_id": case_id, "arm": arm})
                sequence_similarity, shared_line_ratio = 1.0, 1.0
            else:
                sequence_similarity, shared_line_ratio = _similarity(candidate, prior)
            max_sequence = max(
                max_sequence, (sequence_similarity, case_id, arm)
            )
            max_shared_lines = max(
                max_shared_lines, (shared_line_ratio, case_id, arm)
            )
            if candidate == prior:
                continue
            if (
                sequence_similarity >= max_sequence_similarity
                or shared_line_ratio >= max_shared_line_ratio
            ):
                triggered_by = []
                if sequence_similarity >= max_sequence_similarity:
                    triggered_by.append("sequence_similarity")
                if shared_line_ratio >= max_shared_line_ratio:
                    triggered_by.append("shared_line_ratio")
                near_duplicates.append(
                    {
                        "case_id": case_id,
                        "arm": arm,
                        "sequence_similarity": round(sequence_similarity, 6),
                        "shared_line_ratio": round(shared_line_ratio, 6),
                        "triggered_by": triggered_by,
                    }
                )
        comparison_passed = not exact_duplicates and not near_duplicates
        passed = passed and comparison_passed
        comparisons.append(
            {
                "reference_run": str(reference_run),
                "reference_outputs": str(reference_output),
                "passed": comparison_passed,
                "exact_duplicates": exact_duplicates,
                "near_duplicates": near_duplicates,
                "max_observed": {
                    "sequence_similarity": {
                        "value": round(max_sequence[0], 6),
                        "case_id": max_sequence[1],
                        "arm": max_sequence[2],
                    },
                    "shared_line_ratio": {
                        "value": round(max_shared_lines[0], 6),
                        "case_id": max_shared_lines[1],
                        "arm": max_shared_lines[2],
                    },
                },
            }
        )

    return {
        "passed": passed,
        "sample_count": len(current),
        "thresholds": {
            "max_sequence_similarity": max_sequence_similarity,
            "max_shared_line_ratio": max_shared_line_ratio,
            "near_duplicate_triggers_on_either": True,
        },
        "comparisons": comparisons,
        "limitations": [
            "Similarity detection can identify likely reuse but cannot prove independent generation.",
            "Fresh isolated contexts and an auditable execution record remain procedural requirements.",
            "A threshold failure requires regeneration or explicit publication as a non-independent variant.",
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

    import_antigravity = subparsers.add_parser(
        "import-antigravity",
        help="import manually generated Antigravity Markdown responses",
    )
    import_antigravity.add_argument("run_dir", type=Path)
    import_antigravity.add_argument("responses", type=Path)
    import_antigravity.add_argument("--metadata", type=Path, required=True)
    import_antigravity.add_argument("--output", type=Path, required=True)

    score = subparsers.add_parser("score", help="score a completed paired run")
    score.add_argument("run_dir", type=Path)
    score.add_argument("outputs", type=Path)
    score.add_argument("--report", type=Path)

    freshness = subparsers.add_parser(
        "verify-freshness",
        help="reject exact or high-confidence near-copy reuse across runs",
    )
    freshness.add_argument("run_dir", type=Path)
    freshness.add_argument("outputs", type=Path)
    freshness.add_argument(
        "--against",
        nargs=2,
        action="append",
        required=True,
        metavar=("RUN_DIR", "OUTPUTS"),
        help="reference run directory and its outputs.jsonl; repeat as needed",
    )
    freshness.add_argument(
        "--max-sequence-similarity",
        type=float,
        default=DEFAULT_MAX_SEQUENCE_SIMILARITY,
    )
    freshness.add_argument(
        "--max-shared-line-ratio",
        type=float,
        default=DEFAULT_MAX_SHARED_LINE_RATIO,
    )
    freshness.add_argument("--report", type=Path)
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
        if args.command == "import-antigravity":
            metadata = import_antigravity_responses(
                args.run_dir,
                args.responses,
                args.metadata,
                args.output,
            )
            print(
                f"OK: imported {metadata['sample_count']} Antigravity responses "
                f"to {args.output}"
            )
            return 0
        if args.command == "verify-freshness":
            report = verify_freshness(
                args.run_dir,
                args.outputs,
                [(Path(run), Path(outputs)) for run, outputs in args.against],
                max_sequence_similarity=args.max_sequence_similarity,
                max_shared_line_ratio=args.max_shared_line_ratio,
            )
            serialized = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
            if args.report:
                args.report.write_text(serialized, encoding="utf-8")
            print(serialized, end="")
            return 0 if report["passed"] else 2
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
