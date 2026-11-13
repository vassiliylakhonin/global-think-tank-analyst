#!/usr/bin/env python3
"""Compatibility entry point. Scoring lives in the installed gtta package."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gtta.forecasts import load, score, main  # noqa: E402,F401

if __name__ == "__main__":
    raise SystemExit(
        main(
            [sys.argv[0], *(sys.argv[1:] or [str(Path(__file__).with_name("log.csv"))])]
        )
    )
