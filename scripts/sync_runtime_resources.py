#!/usr/bin/env python3
"""Copy canonical skill files into the installable Python package."""

from pathlib import Path
from shutil import copyfile


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "src" / "gtta" / "skills"


def main() -> int:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    for filename in ("SKILL.md", "SKILL_RU.md"):
        copyfile(ROOT / filename, DESTINATION / filename)
    print("synced SKILL.md and SKILL_RU.md into src/gtta/skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
