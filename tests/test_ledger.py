"""Synthetic fixtures only. Never write test forecasts to the real log."""

import json
from datetime import date
import pytest
from typer.testing import CliRunner
from gtta.cli import app
from gtta.forecasts import score, load
from gtta.ledger import add_forecast, resolve_forecast


def entry(i="F1", p=80):
    return {
        "id": i,
        "logged_on": "2026-11-01",
        "claim": "Synthetic event happens.",
        "probability": p,
        "resolve_by": "2026-12-01",
        "resolution_rule": "Synthetic source says yes.",
    }


def test_add_resolve_score_and_immutability(tmp_path):
    path = tmp_path / "log.csv"
    add_forecast(path, entry())
    original = path.read_bytes()
    with pytest.raises(ValueError):
        add_forecast(path, entry())
    assert path.read_bytes() == original
    resolve_forecast(path, "F1", "yes", date(2026, 12, 1), "Synthetic source")
    result = score(load(path), date(2026, 12, 2))
    assert result["brier"] == pytest.approx(0.04)
    with pytest.raises(ValueError):
        resolve_forecast(path, "F1", "no", date(2026, 12, 1), "changed mind")
    assert load(path)[0]["probability"] == "80"
    assert "Synthetic source" in load(path)[0]["notes"]


@pytest.mark.parametrize(
    "patch",
    [
        {"probability": True},
        {"probability": 100},
        {"probability": 0},
        {"probability": 80.5},
        {"claim": ""},
        {"resolve_by": "2026-01-01"},
        {"outcome": "yes"},
    ],
)
def test_invalid_new_forecasts_do_not_write(tmp_path, patch):
    path = tmp_path / "log.csv"
    with pytest.raises(ValueError):
        add_forecast(path, {**entry(), **patch})
    assert not path.exists()


def test_pending_void_and_empty_score():
    rows = [
        {"id": "1", "probability": "80", "outcome": "", "resolve_by": "2026-11-01"},
        {"id": "2", "probability": "50", "outcome": "void", "resolve_by": "2026-11-01"},
    ]
    result = score(rows, date(2026, 12, 1))
    assert result == {"resolved": 0, "pending": 1, "overdue": ["1"]}
    assert "brier" not in score([])
    with pytest.raises(ValueError):
        score(rows + rows)


def test_lock_and_invalid_resolution_leave_ledger_unchanged(tmp_path):
    path = tmp_path / "log.csv"
    add_forecast(path, entry())
    before = path.read_bytes()
    for args in [
        ("F9", "yes", date(2026, 12, 1), "basis"),
        ("F1", "maybe", date(2026, 12, 1), "basis"),
        ("F1", "yes", date(2025, 1, 1), "basis"),
        ("F1", "yes", date(2026, 12, 1), " "),
    ]:
        with pytest.raises(ValueError):
            resolve_forecast(path, *args)
        assert path.read_bytes() == before
    lock = tmp_path / "log.csv.lock"
    lock.mkdir()
    with pytest.raises(ValueError, match="locked"):
        add_forecast(path, entry("F2"))
    assert path.read_bytes() == before


def test_cli_roundtrip(tmp_path):
    runner = CliRunner()
    payload = tmp_path / "entry.json"
    payload.write_text(json.dumps(entry()))
    ledger = tmp_path / "log.csv"
    result = runner.invoke(app, ["forecast-add", str(payload), "--ledger", str(ledger)])
    assert result.exit_code == 0, result.output
    result = runner.invoke(
        app,
        [
            "forecast-resolve",
            "F1",
            "--ledger",
            str(ledger),
            "--outcome",
            "yes",
            "--resolved-on",
            "2026-12-01",
            "--source",
            "synthetic basis",
        ],
    )
    assert result.exit_code == 0, result.output
    result = runner.invoke(
        app, ["forecast-score", str(ledger), "--as-of", "2026-12-02"]
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output)["brier"] == pytest.approx(0.04)
    assert json.loads(result.output)["calibration_claim_supported"] is False
