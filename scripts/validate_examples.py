#!/usr/bin/env python3
"""Validate example evidence-mode and retrieval-date discipline."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"
LIVE_RETRIEVAL_DATE = "2026-05-08"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    examples = sorted(path for path in EXAMPLES_DIR.glob("*.md") if path.name != "README.md")
    if not examples:
        fail("examples/: no markdown examples found")

    for path in examples:
        text = path.read_text(encoding="utf-8")
        lower = text.lower()

        if "evidence mode" not in lower:
            fail(f"{path.relative_to(ROOT)}: missing evidence mode")

        if path.name.startswith("live-source-backed-"):
            if "evidence mode: `live-source-backed`" not in lower and "evidence mode: live-source-backed" not in lower:
                fail(f"{path.relative_to(ROOT)}: live-source-backed example missing explicit evidence mode")
            if LIVE_RETRIEVAL_DATE not in text:
                fail(f"{path.relative_to(ROOT)}: missing retrieval date {LIVE_RETRIEVAL_DATE}")
            if not re.search(r"Retrieved on 2026-05-08|Sources retrieved on \*\*2026-05-08\*\*", text):
                fail(f"{path.relative_to(ROOT)}: retrieval date is not stated in the expected form")
            continue

        if "evidence mode: `live-source-backed`" in lower or "evidence mode: live-source-backed" in lower:
            fail(f"{path.relative_to(ROOT)}: non-live-source-backed filename claims live-source-backed mode")

        if "evidence mode: `mixed`" in lower or "evidence mode: mixed" in lower:
            continue

        if (
            "no live sources were checked" in lower
            or "no live verification performed" in lower
            or "does not cite live sources" in lower
            or "user-provided sources" in lower
        ):
            continue

        fail(f"{path.relative_to(ROOT)}: non-live example must state no live sources or user-provided sources")

    print("ok: examples validated")


if __name__ == "__main__":
    main()
