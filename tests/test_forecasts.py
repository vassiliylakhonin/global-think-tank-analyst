"""Tests for the forecast scorer. All rows here are SYNTHETIC test fixtures."""

import sys
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "forecasts"))
import score  # noqa: E402


def row(i, p, outcome="", resolve_by="2030-01-01"):
    return {"id": i, "probability": str(p), "outcome": outcome, "resolve_by": resolve_by}


class ForecastScoreTests(unittest.TestCase):
    def test_shipped_log_is_empty_and_valid(self):
        rows = score.load(ROOT / "forecasts" / "log.csv")
        self.assertEqual(rows, [], "log must contain only real forecasts; none logged yet")

    def test_brier_synthetic(self):
        result = score.score([row("a", 80, "yes"), row("b", 80, "no")], date(2026, 1, 1))
        self.assertAlmostEqual(result["brier"], (0.04 + 0.64) / 2)
        self.assertAlmostEqual(result["base_rate"], 0.5)

    def test_void_and_pending_excluded(self):
        result = score.score(
            [row("a", 60, "void"), row("b", 60, ""), row("c", 60, "yes")], date(2026, 1, 1)
        )
        self.assertEqual(result["resolved"], 1)
        self.assertEqual(result["pending"], 1)

    def test_overdue_flagged(self):
        result = score.score([row("a", 60, "", "2025-01-01")], date(2026, 1, 1))
        self.assertEqual(result["overdue"], ["a"])

    def test_rejects_bad_probability_and_outcome(self):
        with self.assertRaises(ValueError):
            score.score([row("a", 100, "yes")])
        with self.assertRaises(ValueError):
            score.score([row("a", 50, "maybe")])


if __name__ == "__main__":
    unittest.main()
