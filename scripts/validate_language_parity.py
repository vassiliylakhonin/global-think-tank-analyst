#!/usr/bin/env python3
"""Keep the declared Russian method coverage matching the actual coverage.

`SKILL_RU.md` is not a translation of `SKILL.md`; it is a subset. Both files are
packaged in the wheel and `get_skill_prompt(language="ru")` is a documented
entry point, so an agent can load the Russian method believing it carries the
same contract as the English one. It does not.

This check does not require parity. Partial localisation is a legitimate state.
It requires that the gap is *declared where it is loaded*: `SKILL_RU.md` must
carry a coverage banner whose numbers and missing-mode list match what the files
actually contain, so the claim cannot quietly rot as either file changes.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGLISH = ROOT / "SKILL.md"
RUSSIAN = ROOT / "SKILL_RU.md"

SECTION_RE = re.compile(r"^#{2,3}\s+(.+?)\s*$", re.MULTILINE)
# Modes are counted from section headings, never from prose. The coverage
# banner names the modes it is missing, and a free-text match would read those
# mentions back as definitions.
MODE_HEADING_RE = re.compile(r"^#{2,3}\s+Mode ([A-G])\b", re.MULTILINE)
BANNER_MARKER = "> **Покрытие метода:**"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def measure(path: Path) -> tuple[int, set[str]]:
    text = path.read_text(encoding="utf-8")
    return len(SECTION_RE.findall(text)), set(MODE_HEADING_RE.findall(text))


def main() -> None:
    for path in (ENGLISH, RUSSIAN):
        if not path.exists():
            fail(f"{path.relative_to(ROOT)} is missing")

    english_sections, english_modes = measure(ENGLISH)
    russian_sections, russian_modes = measure(RUSSIAN)
    missing_modes = sorted(english_modes - russian_modes)

    russian_text = RUSSIAN.read_text(encoding="utf-8")
    if BANNER_MARKER not in russian_text:
        fail(
            f"{RUSSIAN.name} must open with a coverage banner starting "
            f"{BANNER_MARKER!r}. The Russian method is a subset of the English one, "
            "and the file itself is what an agent loads — the disclosure has to live "
            "there, not only in the README."
        )

    expected = f"{russian_sections} из {english_sections}"
    if expected not in russian_text:
        fail(
            f"{RUSSIAN.name} coverage banner does not state the measured section count. "
            f"Expected the text {expected!r} (Russian sections / English sections). "
            "Update the banner whenever either file gains or loses a section."
        )

    if missing_modes:
        expected_modes = ", ".join(f"Mode {mode}" for mode in missing_modes)
        if expected_modes not in russian_text:
            fail(
                f"{RUSSIAN.name} coverage banner must name the memo modes it does not "
                f"define. Expected the text {expected_modes!r}. An agent asked for a "
                "mode with no Russian definition has nothing to follow."
            )
    elif "не определены" in russian_text:
        fail(
            f"{RUSSIAN.name} claims missing modes, but every English memo mode is now "
            "present. Update the banner."
        )

    print(
        f"ok: Russian method declares its coverage — {russian_sections} of "
        f"{english_sections} sections"
        + (f", missing {', '.join(missing_modes)}" if missing_modes else ", all modes present")
    )


if __name__ == "__main__":
    main()
