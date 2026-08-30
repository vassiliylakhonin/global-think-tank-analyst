import json

from gtta.artifact import (
    ARTIFACT_SCHEMA_VERSION,
    MemoArtifact,
    check_memo_artifact,
    get_memo_artifact_schema,
    render_memo_artifact,
)
from gtta.discipline import check_contract


def valid_mode_b() -> dict[str, object]:
    return {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "artifact_id": "pilot-decision-001",
        "title": "Reversible pilot decision",
        "question": "Should the operator run a limited pilot?",
        "decision": "Choose whether to authorize a 30-day pilot.",
        "audience": "Operating committee",
        "time_horizon": "30–90 days",
        "mode": "B",
        "evidence_mode": "reasoning-only",
        "bottom_line": {
            "text": "A reversible pilot is preferable to a full rollout.",
            "claim_ids": ["c2"],
        },
        "claims": [
            {
                "claim_id": "c1",
                "text": "The decision can be staged without committing the full budget.",
                "kind": "assumption",
                "provenance": "inference",
                "confidence": "Moderate",
            },
            {
                "claim_id": "c2",
                "text": "A limited pilot preserves more option value than immediate rollout.",
                "kind": "assessment",
                "provenance": "analyst-judgment",
                "basis_claim_ids": ["c1"],
                "confidence": "Moderate",
            },
        ],
        "sections": {
            "actors": {
                "text": "The operator values speed while the committee values reversibility.",
                "claim_ids": ["c1"],
            }
        },
        "options": [
            {
                "option_id": "o1",
                "title": "Authorize a limited pilot",
                "benefit": "Tests the operating assumptions before scaling.",
                "downside": "Delays the full benefit if the concept is already sound.",
                "conditions": "Use only if the pilot has a measurable exit criterion.",
                "basis_claim_ids": ["c1", "c2"],
            }
        ],
        "confidence": "Moderate",
        "key_unknowns": ["Whether the pilot can reproduce full-scale constraints."],
        "change_conditions": [
            "Evidence that the decision is irreversible even at pilot scale."
        ],
        "limitations": ["No external sources were consulted."],
    }


def test_valid_artifact_normalizes_and_passes():
    report = check_memo_artifact(valid_mode_b())
    assert report.passed is True
    assert isinstance(report.artifact, MemoArtifact)
    assert report.to_dict()["scope"] == "memo-artifact-structure-only"
    assert report.to_dict()["artifact"]["mode"] == "B"


def test_schema_is_versioned_and_public():
    schema = get_memo_artifact_schema()
    assert schema["title"] == "MemoArtifact"
    assert ARTIFACT_SCHEMA_VERSION in json.dumps(schema)


def test_rendered_memo_carries_provenance_and_basis_links():
    report = check_memo_artifact(valid_mode_b())
    assert report.artifact is not None
    rendered = render_memo_artifact(report.artifact)
    assert "**Evidence mode:** reasoning-only" in rendered
    assert "[analyst-judgment]" in rendered
    assert "[basis: c2]" in rendered
    assert "## Options" in rendered
    assert "## What would change the judgment" in rendered
    assert check_contract(rendered, mode="B").findings == ()


def test_invalid_json_is_reported_without_an_exception():
    report = check_memo_artifact("{not-json")
    assert report.passed is False
    assert report.findings[0].code == "ARTIFACT001"


def test_missing_claim_provenance_is_rejected():
    payload = valid_mode_b()
    del payload["claims"][0]["provenance"]  # type: ignore[index]
    report = check_memo_artifact(payload)
    assert report.passed is False
    assert any(
        finding.code == "ARTIFACT003" and "provenance" in finding.path
        for finding in report.findings
    )


def test_source_backed_claim_requires_named_source():
    payload = valid_mode_b()
    payload["claims"][0]["provenance"] = "primary"  # type: ignore[index]
    report = check_memo_artifact(payload)
    assert report.passed is False
    assert "source_ref" in report.findings[0].message


def test_fact_cannot_be_declared_as_analyst_judgment():
    payload = valid_mode_b()
    payload["claims"][0]["kind"] = "fact"  # type: ignore[index]
    payload["claims"][0]["provenance"] = "analyst-judgment"  # type: ignore[index]
    report = check_memo_artifact(payload)
    assert report.passed is False
    assert "fact claims require source-backed" in report.findings[0].message


def test_reasoning_only_cannot_claim_primary_provenance():
    payload = valid_mode_b()
    payload["claims"][0]["provenance"] = "primary"  # type: ignore[index]
    payload["claims"][0]["source_refs"] = ["document-1"]  # type: ignore[index]
    report = check_memo_artifact(payload)
    assert report.passed is False
    assert "reasoning-only" in report.findings[0].message


def test_claim_dependency_cycle_is_rejected():
    payload = valid_mode_b()
    payload["claims"][0]["basis_claim_ids"] = ["c2"]  # type: ignore[index]
    report = check_memo_artifact(payload)
    assert report.passed is False
    assert "cycle" in report.findings[0].message


def test_unknown_and_orphaned_claim_references_are_rejected():
    unknown = valid_mode_b()
    unknown["bottom_line"]["claim_ids"] = ["missing"]  # type: ignore[index]
    assert check_memo_artifact(unknown).passed is False

    orphaned = valid_mode_b()
    orphaned["bottom_line"]["claim_ids"] = []  # type: ignore[index]
    orphaned["sections"]["actors"]["claim_ids"] = ["c1"]  # type: ignore[index]
    orphaned["options"][0]["basis_claim_ids"] = ["c1"]  # type: ignore[index]
    report = check_memo_artifact(orphaned)
    assert report.passed is False
    assert "ledger claims must be used" in report.findings[0].message


def test_cli_artifact_check_and_render(tmp_path):
    from typer.testing import CliRunner

    from gtta.cli import app

    artifact_path = tmp_path / "memo.json"
    artifact_path.write_text(json.dumps(valid_mode_b()), encoding="utf-8")

    checked = CliRunner().invoke(
        app, ["check-artifact", str(artifact_path), "--json"]
    )
    assert checked.exit_code == 0, checked.output
    assert json.loads(checked.output)["passed"] is True

    rendered = CliRunner().invoke(app, ["render-artifact", str(artifact_path)])
    assert rendered.exit_code == 0, rendered.output
    assert "Reversible pilot decision" in rendered.output
    assert "[basis: c2]" in rendered.output
