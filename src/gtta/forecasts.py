#!/usr/bin/env python3
"""Score the forecast log. Standard library only. Read-only."""

import csv
import math
import sys
from datetime import date
from pathlib import Path

LOG = Path("forecasts/log.csv")
MIN_FOR_CALIBRATION = 30
BANDS = ((1, 5), (6, 20), (21, 45), (46, 55), (56, 80), (81, 95), (96, 99))
# Decile bins: bin = p // 10, so 10% lands in the "10-20%" bin and the last
# bin covers 90-100%. Kept next to the coarser BANDS, which are retained so
# old output stays comparable.
DECILES = tuple((i, i + 10) for i in range(0, 100, 10))


def load(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def score(rows, today=None):
    today = today or date.today()
    resolved, pending, overdue = [], 0, []
    ids = set()
    for row in rows:
        if row["id"] in ids:
            raise ValueError("duplicate forecast ID: " + row["id"])
        ids.add(row["id"])
        raw = row["probability"]
        if isinstance(raw, bool) or str(raw) != str(int(raw)):
            raise ValueError("probability must be an integer percent")
        probability = int(raw)
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

        def log_loss(probability, outcome):
            return -(
                outcome * math.log(probability)
                + (1 - outcome) * math.log(1 - probability)
            )

        result["log_score"] = sum(log_loss(p / 100, o) for p, o in resolved) / n
        # A base rate of exactly 0 or 1 has no finite log score (log 0).
        # Reported as None rather than clipped to an invented probability.
        result["log_base_rate"] = (
            sum(log_loss(base, o) for _, o in resolved) / n if 0 < base < 1 else None
        )
        bands = []
        for low, high in BANDS:
            hits = [o for p, o in resolved if low <= p <= high]
            if hits:
                bands.append((f"{low}-{high}%", len(hits), sum(hits) / len(hits)))
        result["bands"] = bands
        deciles = []
        for low, high in DECILES:
            hits = [o for p, o in resolved if low <= p < high]
            if hits:
                deciles.append((f"{low}-{high}%", len(hits), sum(hits) / len(hits)))
        result["deciles"] = deciles
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
    print(
        f"Base rate of YES: {result['base_rate']:.0%}; "
        f"Brier of always forecasting it: {result['brier_base_rate']:.3f}"
    )
    print(
        f"Log score: {result['log_score']:.3f} (lower is better; punishes "
        f"confident misses harder than Brier)"
    )
    if result["log_base_rate"] is not None:
        print(f"Log score of always forecasting the base rate: {result['log_base_rate']:.3f}")
    else:
        print("Log score of the base rate: undefined (all resolved outcomes are the same)")
    print("band      n  observed YES")
    for name, n, rate in result["bands"]:
        print(f"{name:8} {n:3}  {rate:.0%}")
    print("decile    n  observed YES")
    for name, n, rate in result["deciles"]:
        print(f"{name:8} {n:3}  {rate:.0%}")
    if result["resolved"] < MIN_FOR_CALIBRATION:
        print(
            f"WARNING: fewer than {MIN_FOR_CALIBRATION} resolved entries. "
            "Not enough to judge calibration."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
