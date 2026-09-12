#!/usr/bin/env python3
"""Run portable golden and negative controls for GTTA memo verification."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import agenda_intelligence

from gtta.artifact import check_memo_artifact
from gtta.sarif import render_verification_sarif
from gtta.verification import (
    load_source_catalog,
    render_memo_repair_prompt,
    verify_memo_artifact,
)


ROOT = Path(__file__).resolve().parents[1]
COOKBOOK = ROOT / "examples" / "cookbooks" / "secondary-sanctions"
SCRIPT_URI = "scripts/run_verification_benchmark.py"


@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    mutation: str
    expected_passed: bool
    expected_status: str
    expected_gtta_rules: tuple[str, ...] = ()
    expected_agenda_issues: tuple[str, ...] = ()


CASES = (
    BenchmarkCase("golden-with-quotes", "none", True, "packet_complete"),
    BenchmarkCase("golden-without-quotes", "remove_quotes", True, "packet_complete"),
    BenchmarkCase(
        "missing-verify-marker",
        "remove_verify_from_c2",
        False,
        "packet_complete",
        expected_gtta_rules=("GTTAV001",),
    ),
    BenchmarkCase(
        "missing-source-record",
        "remove_shipping_source",
        False,
        "packet_incomplete",
        expected_agenda_issues=("missing_source:shipping-record",),
    ),
    BenchmarkCase(
        "tampered-number",
        "replace_24_with_29",
        False,
        "source_review_required",
        expected_agenda_issues=("lexical_support_weak", "unmatched_numbers"),
    ),
    BenchmarkCase(
        "unsupported-claim",
        "replace_c1_with_unsupported_assurance",
        False,
        "source_review_required",
        expected_agenda_issues=("lexical_support_unsupported",),
    ),
)


BENCHMARK_RULES = (
    {
        "id": "GTTABENCH001",
        "shortDescription": {
            "text": "Observed verification behavior matches the frozen expectation"
        },
        "defaultConfiguration": {"level": "error"},
    },
    {
        "id": "GTTABENCH002",
        "shortDescription": {
            "text": "Repair guidance preserves anti-fabrication constraints"
        },
        "defaultConfiguration": {"level": "error"},
    },
    {
        "id": "GTTABENCH003",
        "shortDescription": {"text": "Canonical cookbook inputs remain unchanged"},
        "defaultConfiguration": {"level": "error"},
    },
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run deterministic GTTA -> Agenda verification controls."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "artifacts" / "verification-benchmark.json",
        help="Summary JSON destination.",
    )
    parser.add_argument(
        "--sarif",
        type=Path,
        default=ROOT / "artifacts" / "verification-benchmark.sarif",
        help="SARIF 2.1.0 destination.",
    )
    return parser.parse_args()


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def source_input_hashes() -> dict[str, str]:
    paths = [COOKBOOK / "memo.json", COOKBOOK / "memo.sources.json"]
    paths.extend(path for path in sorted((COOKBOOK / "sources").rglob("*")) if path.is_file())
    return {str(path.relative_to(ROOT)): sha256_file(path) for path in paths}


def claim(memo: dict[str, Any], claim_id: str) -> dict[str, Any]:
    return next(item for item in memo["claims"] if item["claim_id"] == claim_id)


def apply_mutation(
    mutation: str, memo: dict[str, Any], catalog: dict[str, Any]
) -> None:
    if mutation == "none":
        return
    if mutation == "remove_quotes":
        catalog["quotes"] = []
        return
    if mutation == "remove_verify_from_c2":
        claim(memo, "c2")["verify"] = False
        return
    if mutation == "remove_shipping_source":
        catalog["sources"] = [
            item
            for item in catalog["sources"]
            if item["source_id"] != "shipping-record"
        ]
        return
    if mutation == "replace_24_with_29":
        target = claim(memo, "c1")
        target["text"] = target["text"].replace("24 microcontroller", "29 microcontroller")
        return
    if mutation == "replace_c1_with_unsupported_assurance":
        claim(memo, "c1")["text"] = (
            "Every counterparty is legally cleared and every shipment is risk-free."
        )
        return
    raise ValueError(f"Unknown mutation: {mutation}")


def agenda_issues(report_dict: dict[str, Any]) -> list[str]:
    response = (report_dict.get("agenda") or {}).get("response") or {}
    return [
        str(issue)
        for claim_result in response.get("claims", []) or []
        for issue in claim_result.get("issues", []) or []
    ]


def benchmark_error(case_id: str, message: str, rule_id: str) -> dict[str, Any]:
    return {
        "ruleId": rule_id,
        "level": "error",
        "message": {"text": f"{case_id}: {message}"},
        "locations": [
            {
                "physicalLocation": {
                    "artifactLocation": {"uri": SCRIPT_URI},
                    "region": {"startLine": 1},
                }
            }
        ],
        "properties": {"benchmarkCase": case_id},
    }


def run_case(
    case: BenchmarkCase,
    baseline_memo: dict[str, Any],
    baseline_catalog: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    memo = copy.deepcopy(baseline_memo)
    catalog = copy.deepcopy(baseline_catalog)
    apply_mutation(case.mutation, memo, catalog)
    memo_text = canonical_json(memo)
    catalog_text = canonical_json(catalog)

    artifact_check = check_memo_artifact(memo)
    if artifact_check.artifact is None:
        messages = "; ".join(finding.message for finding in artifact_check.findings)
        raise RuntimeError(f"Invalid generated case {case.case_id}: {messages}")

    report = verify_memo_artifact(
        artifact_check.artifact,
        source_catalog=load_source_catalog(catalog),
        base_dir=COOKBOOK,
        strict=True,
    )
    report_dict = report.to_dict()
    repair_prompt = render_memo_repair_prompt(report)
    actual_gtta_rules = [item["rule_id"] for item in report_dict["gtta_findings"]]
    actual_agenda_issues = agenda_issues(report_dict)

    assertions = [
        {
            "name": "verification_passed_matches",
            "passed": report.passed is case.expected_passed,
            "expected": case.expected_passed,
            "actual": report.passed,
        },
        {
            "name": "packet_status_matches",
            "passed": report.packet_status == case.expected_status,
            "expected": case.expected_status,
            "actual": report.packet_status,
        },
        {
            "name": "expected_gtta_rules_present",
            "passed": set(case.expected_gtta_rules).issubset(actual_gtta_rules),
            "expected": list(case.expected_gtta_rules),
            "actual": actual_gtta_rules,
        },
        {
            "name": "expected_agenda_issues_present",
            "passed": set(case.expected_agenda_issues).issubset(actual_agenda_issues),
            "expected": list(case.expected_agenda_issues),
            "actual": actual_agenda_issues,
        },
    ]

    if case.expected_passed:
        assertions.append(
            {
                "name": "complete_prompt_is_non_repair_status",
                "passed": repair_prompt.startswith("# GTTA Memo Repair Status: Complete"),
                "expected": "complete status",
                "actual": repair_prompt.splitlines()[0],
            }
        )
    else:
        for phrase in (
            "do not manufacture evidence",
            "Never invent a source ID",
            "Do not claim success unless",
        ):
            assertions.append(
                {
                    "name": f"repair_prompt_contains:{phrase}",
                    "passed": phrase in repair_prompt,
                    "expected": phrase,
                    "actual": "present" if phrase in repair_prompt else "missing",
                }
            )

    benchmark_passed = all(item["passed"] for item in assertions)
    native_sarif = render_verification_sarif(
        report,
        artifact_uri="examples/cookbooks/secondary-sanctions/memo.json",
        artifact_text=memo_text,
    )
    result = {
        "case_id": case.case_id,
        "mutation": case.mutation,
        "negative_control": not case.expected_passed,
        "benchmark_passed": benchmark_passed,
        "verification_passed": report.passed,
        "packet_status": report.packet_status,
        "detected_gtta_rules": actual_gtta_rules,
        "detected_agenda_issues": actual_agenda_issues,
        "memo_sha256": sha256_bytes(memo_text.encode()),
        "source_catalog_sha256": sha256_bytes(catalog_text.encode()),
        "assertions": assertions,
    }
    return result, native_sarif


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(payload), encoding="utf-8")


def main() -> int:
    args = parse_args()
    before_hashes = source_input_hashes()
    baseline_memo = json.loads((COOKBOOK / "memo.json").read_text(encoding="utf-8"))
    baseline_catalog = json.loads(
        (COOKBOOK / "memo.sources.json").read_text(encoding="utf-8")
    )

    cases: list[dict[str, Any]] = []
    sarif_results: list[dict[str, Any]] = []
    native_rules: list[dict[str, Any]] = []
    for case in CASES:
        result, native_sarif = run_case(case, baseline_memo, baseline_catalog)
        cases.append(result)
        native_run = native_sarif["runs"][0]
        if not native_rules:
            native_rules = native_run["tool"]["driver"]["rules"]
        native_results = native_run["results"]

        if case.expected_passed:
            sarif_results.extend(native_results)
        else:
            for item in native_results:
                expected_item = copy.deepcopy(item)
                expected_item["level"] = "note"
                expected_item.pop("locations", None)
                expected_item.setdefault("properties", {}).update(
                    {
                        "benchmarkCase": case.case_id,
                        "expectedNegativeControl": True,
                    }
                )
                expected_item["message"]["text"] = (
                    f"Expected negative control {case.case_id}: "
                    + expected_item["message"]["text"]
                )
                sarif_results.append(expected_item)

        for assertion in result["assertions"]:
            if assertion["passed"]:
                continue
            rule_id = (
                "GTTABENCH002"
                if assertion["name"].startswith("repair_prompt")
                else "GTTABENCH001"
            )
            sarif_results.append(
                benchmark_error(
                    case.case_id,
                    (
                        f"assertion {assertion['name']} failed; expected "
                        f"{assertion['expected']!r}, got {assertion['actual']!r}"
                    ),
                    rule_id,
                )
            )

    after_hashes = source_input_hashes()
    source_inputs_unchanged = before_hashes == after_hashes
    if not source_inputs_unchanged:
        sarif_results.append(
            benchmark_error(
                "benchmark-run",
                "canonical cookbook inputs changed during execution",
                "GTTABENCH003",
            )
        )

    passed = all(case["benchmark_passed"] for case in cases) and source_inputs_unchanged
    summary = {
        "schema_version": "gtta.memo-verification-benchmark@1.0",
        "passed": passed,
        "agenda_version": agenda_intelligence.__version__,
        "case_count": len(cases),
        "passed_case_count": sum(case["benchmark_passed"] for case in cases),
        "golden_case_count": sum(not case["negative_control"] for case in cases),
        "negative_control_count": sum(case["negative_control"] for case in cases),
        "source_inputs_unchanged": source_inputs_unchanged,
        "canonical_input_sha256": before_hashes,
        "cases": cases,
        "limitations": (
            "The benchmark establishes deterministic contract behavior only; it does not "
            "assess factual truth, source authority, legal sufficiency, or decision safety."
        ),
    }
    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "gtta-memo-verification-benchmark",
                        "semanticVersion": "1.0.0",
                        "informationUri": (
                            "https://github.com/vassiliylakhonin/"
                            "global-think-tank-analyst"
                        ),
                        "rules": native_rules + list(BENCHMARK_RULES),
                    }
                },
                "invocations": [{"executionSuccessful": passed}],
                "results": sarif_results,
                "properties": {
                    "scope": "golden-and-negative-control-benchmark",
                    "expectedNegativeFindingsAreNotes": True,
                },
            }
        ],
    }
    write_json(args.out, summary)
    write_json(args.sarif, sarif)
    print(canonical_json(summary), end="")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
