#!/usr/bin/env python3
"""Keep the Russian runtime method structurally aligned with the canonical one.

Both skill files are packaged and exposed through ``get_skill_prompt``. The
Russian rendering therefore has to retain every method section, every memo
mode, and the machine-checkable labels that callers rely on.
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
REQUIRED_RUNTIME_MARKERS = (
    "полный русскоязычный эквивалент",
    "EVIDENCE ACCESS LIMITED: no live verification performed in this environment.",
    "[primary]",
    "[secondary]",
    "[user-provided]",
    "[inference]",
    "[analyst-judgment]",
    "[verify]",
    "[stale-risk: YYYY-MM]",
    "**Question:**",
    "**Decision:**",
    "**Audience:**",
    "**Time horizon:**",
    "**Evidence mode:**",
    "Risk Severity",
    "Decision Relevance",
    "Executive Takeaway",
    "Decision Context",
    "What Is Known / Evidence Limits",
    "Actors and Incentives",
    "Main Assessment",
    "Risks and Trade-Offs",
    "Indicators to Watch",
    "What Would Change This Judgment",
)


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
    extra_modes = sorted(russian_modes - english_modes)

    russian_text = RUSSIAN.read_text(encoding="utf-8")
    if BANNER_MARKER not in russian_text:
        fail(
            f"{RUSSIAN.name} must open with a coverage banner starting "
            f"{BANNER_MARKER!r}; the parity claim must live in the runtime file."
        )

    if russian_sections != english_sections:
        fail(
            f"{RUSSIAN.name} has {russian_sections} method sections; "
            f"{ENGLISH.name} has {english_sections}. Full structural parity is required."
        )

    expected = f"{english_sections} из {english_sections}"
    if expected not in russian_text:
        fail(
            f"{RUSSIAN.name} parity banner must contain {expected!r}."
        )

    if missing_modes:
        fail(
            f"{RUSSIAN.name} is missing memo modes: {', '.join(missing_modes)}."
        )
    if extra_modes:
        fail(f"{RUSSIAN.name} has unknown memo modes: {', '.join(extra_modes)}.")

    missing_markers = [
        marker for marker in REQUIRED_RUNTIME_MARKERS if marker not in russian_text
    ]
    if missing_markers:
        fail(
            f"{RUSSIAN.name} is missing runtime contract markers: "
            + ", ".join(repr(marker) for marker in missing_markers)
        )

    print(
        f"ok: Russian method parity — {russian_sections}/{english_sections} "
        f"sections and all {len(english_modes)} modes present"
    )


if __name__ == "__main__":
    main()
