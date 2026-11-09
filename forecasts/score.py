#!/usr/bin/env python3
"""Score the forecast log. Standard library only. Read-only."""

import csv
import sys
from datetime import date
from pathlib import Path

LOG = Path(__file__).resolve().parent / "log.csv"
MIN_FOR_CALIBRATION = 30
BANDS = ((1, 5), (6, 20), (21, 45), (46, 55), (56, 80), (81, 95), (96, 99))


def load(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def score(rows, today=None):
    today = today or date.today()
    resolved, pending, overdue = [], 0, []
    for row in rows:
        probability = int(row["probability"])
        if not 1 <= probability <= 99:
            raise ValueError(f"{row['id']}: probability must be 1-99")
        outcome = (row.get("outcome") or "").strip().lower()
        if outcome in ("yes", "no"):
            resolved.append((probability, 1 if outcome == "yes" else 0))
        elif outcome == "void":
            continue
        elif outcome:
            raise ValueError(f"{row['id']}: outcome must be yes, no, void or empty")
        else:
            pending += 1
            if date.fromisoformat(row["resolve_by"]) < today:
                overdue.append(row["id"])
    result = {"resolved": len(resolved), "pending": pending, "overdue": overdue}
    if resolved:
        n = len(resolved)
        base = sum(o for _, o in resolved) / n
        result["brier"] = sum((p / 100 - o) ** 2 for p, o in resolved) / n
        result["base_rate"] = base
        result["brier_base_rate"] = sum((base - o) ** 2 for _, o in resolved) / n
        bands = []
        for low, high in BANDS:
            hits = [o for p, o in resolved if low <= p <= high]
            if hits:
                bands.append((f"{low}-{high}%", len(hits), sum(hits) / len(hits)))
        result["bands"] = bands
    return result


def main(argv):
    path = Path(argv[1]) if len(argv) > 1 else LOG
    result = score(load(path))
    print(f"resolved: {result['resolved']}  pending: {result['pending']}")
    if result["overdue"]:
        print("OVERDUE, resolve these: " + ", ".join(result["overdue"]))
    if not result["resolved"]:
        print("No resolved forecasts yet. No calibration can be computed.")
        return 0
    print(f"Brier score: {result['brier']:.3f} (lower is better; always-50% = 0.250)")
    print(f"Base rate of YES: {result['base_rate']:.0%}; "
          f"Brier of always forecasting it: {result['brier_base_rate']:.3f}")
    print("band      n  observed YES")
    for name, n, rate in result["bands"]:
        print(f"{name:8} {n:3}  {rate:.0%}")
    if result["resolved"] < MIN_FOR_CALIBRATION:
        print(f"WARNING: fewer than {MIN_FOR_CALIBRATION} resolved entries. "
              "Not enough to judge calibration.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
