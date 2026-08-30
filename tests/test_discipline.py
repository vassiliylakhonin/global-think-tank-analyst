import json

import pytest

from gtta.discipline import RULESET_VERSION, Severity, check_contract


VALID_MODE_B = """# Memo
Evidence mode: reasoning-only

## Executive takeaway
[analyst-judgment] Maintain the current posture.

## Decision context
The decision concerns timing.

## Actors
The operator and regulator have different incentives.

## Options
Use a reversible pilot.

## Confidence
Moderate confidence because evidence access is limited.

## What would change this judgment
A primary-source rule change would alter the posture.
"""


def finding_ids(report):
    return {item.rule_id for item in report.findings}


def test_valid_mode_b_contract_passes_without_findings():
    report = check_contract(VALID_MODE_B, mode="B")
    assert report.passed is True
    assert report.ruleset_version == RULESET_VERSION
    assert report.evidence_mode == "reasoning-only"
    assert report.findings == ()


def test_ruleset_exposes_stable_v1_interface():
    assert RULESET_VERSION == "gtta-method-contract@1.0.0"


def test_missing_required_declarations_are_errors():
    report = check_contract("An unlabelled memo.", mode="A")
    assert report.passed is False
    assert {"GTTA002", "GTTA004"}.issubset(finding_ids(report))
    assert all(
        item.severity is Severity.ERROR
        for item in report.findings
        if item.rule_id in {"GTTA002", "GTTA004"}
    )


def test_unsupported_evidence_mode_is_named():
    report = check_contract(
        "Evidence mode: source-backed public demo\n[analyst-judgment] Draft."
    )
    finding = next(item for item in report.findings if item.rule_id == "GTTA003")
    assert finding.line == 1
    assert report.passed is False


def test_mode_f_does_not_require_provenance_or_confidence():
    report = check_contract(
        "Evidence mode: reasoning-only\n## Coaching questions\nWhat is known?",
        mode="F",
    )
    assert report.passed is True
    assert "GTTA004" not in finding_ids(report)
    assert "GTTA006" not in finding_ids(report)


def test_generic_advice_is_a_warning_with_a_line():
    report = check_contract(
        VALID_MODE_B + "\nThe team should monitor the situation.\n", mode="B"
    )
    finding = next(item for item in report.findings if item.rule_id == "GTTA009")
    assert finding.severity is Severity.WARNING
    assert finding.line is not None
    assert report.passed is True


def test_report_is_machine_readable_and_states_its_limit():
    payload = check_contract(VALID_MODE_B, mode="B").to_dict()
    assert payload["scope"] == "method-contract-only"
    assert payload["passed"] is True
    assert "No factuality" in payload["limitations"]
    json.dumps(payload)


def test_invalid_mode_is_rejected():
    with pytest.raises(ValueError, match="A, B, C"):
        check_contract(VALID_MODE_B, mode="Z")


def test_cli_contract_exit_semantics(tmp_path):
    pytest.importorskip("typer")
    from typer.testing import CliRunner

    from gtta.cli import app

    valid = tmp_path / "valid.md"
    valid.write_text(VALID_MODE_B, encoding="utf-8")
    passing = CliRunner().invoke(
        app, ["check-contract", str(valid), "--mode", "B", "--json"]
    )
    assert passing.exit_code == 0, passing.output
    assert json.loads(passing.output)["passed"] is True

    invalid = tmp_path / "invalid.md"
    invalid.write_text("Unlabelled.", encoding="utf-8")
    failing = CliRunner().invoke(app, ["check-contract", str(invalid), "--mode", "B"])
    assert failing.exit_code == 1
    assert "GTTA002" in failing.output
