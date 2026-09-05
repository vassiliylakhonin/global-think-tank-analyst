import json

import pytest

from gtta.discipline import RULESET_VERSION, Severity, check_contract


VALID_MODE_B = """# Memo
Evidence mode: reasoning-only

## Executive takeaway
[analyst-judgment] Maintain the current posture.

## Decision context
[inference] The decision concerns timing.

## Actors
[analyst-judgment] The operator and regulator have different incentives.

## Options
[analyst-judgment] Use a reversible pilot.

## Confidence
Moderate confidence because evidence access is limited.

## What would change this judgment
[inference] A primary-source rule change would alter the posture.
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
    assert RULESET_VERSION == "gtta-method-contract@1.2.3"


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


def test_quoted_rejection_of_generic_advice_is_not_a_warning():
    report = check_contract(
        VALID_MODE_B
        + "\n[analyst-judgment] Replace \"monitor the situation\" with "
        + "observable if-then decision logic.\n",
        mode="B",
    )
    assert "GTTA009" not in finding_ids(report)


def test_quoted_generic_advice_without_rejection_remains_a_warning():
    report = check_contract(
        VALID_MODE_B
        + '\n[analyst-judgment] The team should "monitor the situation" weekly.\n',
        mode="B",
    )
    assert "GTTA009" in finding_ids(report)


def test_later_generic_advice_is_found_after_a_quoted_rejection():
    report = check_contract(
        VALID_MODE_B
        + "\n[analyst-judgment] Avoid \"monitor the situation\" as empty advice.\n"
        + "The team should monitor the situation.\n",
        mode="B",
    )
    findings = [item for item in report.findings if item.rule_id == "GTTA009"]
    assert len(findings) == 1
    assert findings[0].line == len(VALID_MODE_B.splitlines()) + 3


def test_likely_untagged_claim_is_a_warning_with_a_line():
    report = check_contract(
        VALID_MODE_B
        + "\n## Additional assessment\n"
        + "The regulator is likely to delay implementation beyond the announced date.\n",
        mode="B",
    )
    finding = next(item for item in report.findings if item.rule_id == "GTTA010")
    assert finding.severity is Severity.WARNING
    assert finding.line is not None
    assert report.passed is True


def test_exact_limited_evidence_disclosure_is_not_a_claim_warning():
    report = check_contract(
        VALID_MODE_B
        + "\n**EVIDENCE ACCESS LIMITED: no live verification performed in this "
        + "environment.**\n",
        mode="B",
    )
    assert "GTTA010" not in finding_ids(report)


def test_modified_limited_evidence_sentence_remains_claim_checked():
    report = check_contract(
        VALID_MODE_B
        + "\nEvidence access is limited and the regulator has not been checked live.\n",
        mode="B",
    )
    assert "GTTA010" in finding_ids(report)


def test_exact_finding_limit_is_not_reported_as_truncated():
    claims = "\n".join(
        f"The regulator is likely to delay implementation in scenario {index}."
        for index in range(25)
    )
    report = check_contract(VALID_MODE_B + "\n" + claims, mode="B")
    assert sum(item.rule_id == "GTTA010" for item in report.findings) == 25
    assert report.truncated_rule_ids == ()
    assert report.to_dict()["findings_truncated"] is False


def test_findings_beyond_limit_are_explicitly_reported_as_truncated():
    claims = "\n".join(
        f"The regulator is likely to delay implementation in scenario {index}."
        for index in range(26)
    )
    report = check_contract(VALID_MODE_B + "\n" + claims, mode="B")
    payload = report.to_dict()
    assert sum(item.rule_id == "GTTA010" for item in report.findings) == 25
    assert report.truncated_rule_ids == ("GTTA010",)
    assert payload["findings_truncated"] is True
    assert payload["truncated_rule_ids"] == ["GTTA010"]
    assert payload["finding_limits"] == {"GTTA010": 25}
    assert "findings truncated" in report.render_text()


def test_metadata_headings_and_table_separators_are_not_claims():
    report = check_contract(VALID_MODE_B, mode="B")
    assert "GTTA010" not in finding_ids(report)


def test_metadata_questions_and_table_layout_are_not_claims():
    report = check_contract(
        VALID_MODE_B
        + "\n**To:** Board Risk Committee\n"
        + "Should the Board approve a reversible pilot or retain the status quo?\n\n"
        + "| Option | Benefit | Risk |\n"
        + "|---|---|---|\n"
        + "| **Option A** | [analyst-judgment] Preserves flexibility. | "
        + "A delayed launch could surrender the most valuable customer segment. |\n",
        mode="B",
    )
    warnings = [item for item in report.findings if item.rule_id == "GTTA010"]
    assert len(warnings) == 1
    assert warnings[0].message.endswith("Table column: 3.")


def test_semantically_equivalent_mode_markers_are_accepted():
    report = check_contract(
        """# Scenario brief
Evidence mode: reasoning-only

## Baseline Outlook
[inference] Current conditions persist.

## Scenario Planning
[analyst-judgment] An alternative path remains possible.

## Decision Triggers
[inference] A rule change would alter the path.

## What to Watch
[analyst-judgment] Review observable signals monthly.

Confidence: Moderate.
""",
        mode="C",
    )
    assert "GTTA008" not in finding_ids(report)


def test_bilingual_russian_mode_b_headings_remain_machine_checkable():
    report = check_contract(
        """# Меморандум
Question: следует ли запускать обратимый пилот? (Вопрос)
Decision: запуск, ожидание или отказ. (Решение)
Audience: операционный комитет. (Аудитория)
Time horizon: near-term. (Временной горизонт)
Evidence mode: reasoning-only. (Режим доказательств)

**EVIDENCE ACCESS LIMITED: no live verification performed in this environment.**

## Executive Takeaway / Резюме для руководства
[analyst-judgment] Обратимый пилот выглядит предпочтительнее полного запуска.

## Decision Context / Контекст решения
[inference] Решение касается момента и масштаба входа.

## Actors and Incentives / Акторы и стимулы
[analyst-judgment] Оператор стремится сохранить гибкость.

## Options / Варианты действий
[analyst-judgment] Вариант A — ограниченный пилот.

## Confidence and Key Unknowns / Уверенность и неизвестные
Confidence: Moderate.
""",
        mode="B",
    )
    assert report.passed is True
    assert report.evidence_mode == "reasoning-only"
    assert "GTTA008" not in finding_ids(report)


def test_mode_g_evidence_evaluation_matrix_marker_is_accepted():
    report = check_contract(
        """# Competing hypotheses
Evidence mode: illustrative source packet

## Hypotheses formulation
[analyst-judgment] Multiple explanations remain viable.

## Evidence Evaluation Matrix
[user-provided] The packet contains ambiguous observations.

## Sensitivity analysis
[inference] Physical forensics would change the ranking.

## Bounded judgment
[analyst-judgment] Attribution remains premature.

Confidence: Moderate.
""",
        mode="G",
    )
    assert "GTTA008" not in finding_ids(report)


def test_report_is_machine_readable_and_states_its_limit():
    payload = check_contract(VALID_MODE_B, mode="B").to_dict()
    assert payload["scope"] == "method-contract-only"
    assert payload["passed"] is True
    assert payload["findings_truncated"] is False
    assert payload["truncated_rule_ids"] == []
    assert payload["finding_limits"] == {"GTTA010": 25}
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
