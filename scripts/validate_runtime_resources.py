#!/usr/bin/env python3
"""Ensure committed runtime skill resources match the repository canon."""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAIRS = (
    (ROOT / "SKILL.md", ROOT / "src" / "gtta" / "skills" / "SKILL.md"),
    (ROOT / "SKILL_RU.md", ROOT / "src" / "gtta" / "skills" / "SKILL_RU.md"),
)


def main() -> int:
    for canonical, packaged in PAIRS:
        if not packaged.exists():
            print(f"ERROR: missing runtime resource {packaged.relative_to(ROOT)}", file=sys.stderr)
            return 1
        if canonical.read_bytes() != packaged.read_bytes():
            print(
                f"ERROR: {packaged.relative_to(ROOT)} has drifted from "
                f"{canonical.relative_to(ROOT)}; run scripts/sync_runtime_resources.py",
                file=sys.stderr,
            )
            return 1

    print("ok: packaged EN/RU runtime resources match the canonical skill files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
