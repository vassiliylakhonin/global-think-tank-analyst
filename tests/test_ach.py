import json
import pytest
from typer.testing import CliRunner
from gtta.ach import rank_ach
from gtta.cli import app


def fixture():
    return {
        "hypotheses": ["H1", "H2", "H3"],
        "evidence": ["E1", "E2"],
        "matrix": {
            "E1": {"H1": "inconsistent", "H2": "consistent", "H3": "unknown"},
            "E2": {"H1": "neutral", "H2": "neutral", "H3": "unknown"},
        },
    }


def test_counts_ties_and_unknowns():
    result = rank_ach(fixture())
    assert [(r["hypothesis_id"], r["rank"]) for r in result["ranking"]] == [
        ("H2", 1),
        ("H3", 1),
        ("H1", 3),
    ]
    assert result["ranking"][1]["unknown_count"] == 2
    assert result["ranking"][1]["assessed_count"] == 0
    assert result["ranking"][2]["inconsistent_evidence_ids"] == ["E1"]
    assert result["human_review_required"]


@pytest.mark.parametrize(
    "mutation", ["missing", "extra", "duplicate", "empty", "invalid"]
)
def test_bad_matrix_rejected(mutation):
    payload = fixture()
    if mutation == "missing":
        del payload["matrix"]["E1"]["H1"]
    elif mutation == "extra":
        payload["matrix"]["E3"] = payload["matrix"]["E1"]
    elif mutation == "duplicate":
        payload["hypotheses"].append("H1")
    elif mutation == "empty":
        payload["evidence"] = []
    else:
        payload["matrix"]["E1"]["H1"] = "probably"
    with pytest.raises(ValueError):
        rank_ach(payload)


def test_cli_stdin_and_error():
    result = CliRunner().invoke(app, ["ach", "-"], input=json.dumps(fixture()))
    assert result.exit_code == 0
    assert len(json.loads(result.output)["ranking"]) == 3
    assert CliRunner().invoke(app, ["ach", "-"], input="{}").exit_code == 2
