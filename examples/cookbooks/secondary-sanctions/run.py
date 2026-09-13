"""Run the deterministic GTTA -> Agenda Intelligence verification cookbook."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEMO = HERE / "memo.json"
REVIEW_BUNDLE = HERE / "review-bundle"


def main() -> int:
    command = [
        sys.executable,
        "-m",
        "gtta.cli",
        "review",
        str(MEMO),
        "--out-dir",
        str(REVIEW_BUNDLE),
    ]
    result = subprocess.run(command, cwd=HERE, check=False)
    if result.returncode == 0:
        print(f"Verified illustrative packet; bundle: {REVIEW_BUNDLE}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
