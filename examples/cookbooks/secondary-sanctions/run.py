"""Run the deterministic GTTA -> Agenda Intelligence verification cookbook."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEMO = HERE / "memo.json"
REPORT = HERE / "review.html"
REPAIR = HERE / "repair.md"


def main() -> int:
    command = [
        sys.executable,
        "-m",
        "gtta.cli",
        "verify",
        str(MEMO),
        "--strict",
        "--format",
        "html",
        "--out",
        str(REPORT),
        "--repair-prompt",
        str(REPAIR),
    ]
    result = subprocess.run(command, cwd=HERE, check=False)
    if result.returncode == 0:
        print(f"Verified illustrative packet; review: {REPORT}; repair status: {REPAIR}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
