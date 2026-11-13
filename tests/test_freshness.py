"""Synthetic freshness fixtures, not claims about real evidence."""

import json
from datetime import date
import pytest
from typer.testing import CliRunner
from gtta.cli import app
from gtta.freshness import evidence_age
from gtta.artifact import check_memo_artifact, render_memo_artifact
from test_artifact import valid_mode_b
from test_harvest import REVERSAL


def payload():
    value = valid_mode_b()
    value.update(
        schema_version="gtta.memo@2.0",
        null_hypothesis="If no action is taken, retain the current operating posture.",
        reversal_conditions=[REVERSAL],
        evidence_mode="user-provided sources",
    )
    value["claims"][0].update(
        kind="fact",
        provenance="user-provided",
        source_refs=["SRC-01"],
        evidence_as_of="2026-11-01",
        valid_for_days=10,
    )
    return value


def test_expiry_boundary_and_declared_dependency_blocks():
    before = evidence_age(payload(), date(2026, 11, 10))
    assert before["facts"][0]["status"] == "within-declared-ttl"
    result = evidence_age(payload(), date(2026, 11, 11))
    assert result["expired_fact_ids"] == ["c1"]
    assert result["affected_claim_ids"] == ["c1", "c2"]
    assert any(block["path"] == "bottom_line" for block in result["affected_blocks"])
    assert result["facts"][0]["age_days"] == 10
    assert result["facts"][0]["expires_on"] == "2026-11-11"


def test_unknown_and_future_dates_do_not_claim_freshness():
    value = payload()
    assert (
        evidence_age(value, date(2026, 10, 31))["facts"][0]["status"] == "future-dated"
    )
    del value["claims"][0]["evidence_as_of"]
    del value["claims"][0]["valid_for_days"]
    result = evidence_age(value, date(2026, 11, 13))
    assert result["facts"][0]["status"] == "unknown"
    assert result["expired_fact_ids"] == []


@pytest.mark.parametrize(
    "patch",
    [
        {"valid_for_days": 0},
        {"valid_for_days": True},
        {"valid_for_days": 1.5},
        {"valid_for_days": 40000},
        {"evidence_as_of": "2026-02-30"},
        {"evidence_as_of": "9999-12-31"},
        {"valid_for_days": None},
    ],
)
def test_bad_dates_and_ttl_rejected(patch):
    value = payload()
    value["claims"][0].update(patch)
    assert not check_memo_artifact(value).passed
    with pytest.raises(ValueError):
        evidence_age(value, date(2026, 11, 13))


def test_v1_requires_explicit_migration():
    with pytest.raises(ValueError):
        evidence_age(valid_mode_b(), date(2026, 11, 13))


def test_cli_explicit_date_and_leap_boundary(tmp_path):
    value = payload()
    value["claims"][0].update(evidence_as_of="2028-02-28", valid_for_days=2)
    artifact = tmp_path / "memo.json"
    artifact.write_text(json.dumps(value))
    result = CliRunner().invoke(
        app, ["evidence-age", str(artifact), "--as-of", "2028-03-01"]
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["facts"][0]["status"] == "expired"
    assert (
        CliRunner()
        .invoke(app, ["evidence-age", str(artifact), "--as-of", "tomorrow"])
        .exit_code
        == 2
    )


def test_renderer_exposes_declared_freshness_fields():
    artifact = check_memo_artifact(payload()).artifact
    rendered = render_memo_artifact(artifact)
    assert "[evidence-as-of: 2026-11-01][valid-for-days: 10]" in rendered
