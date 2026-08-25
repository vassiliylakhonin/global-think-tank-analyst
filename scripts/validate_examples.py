#!/usr/bin/env python3
"""Validate canonical example evidence modes and source-date discipline."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"
CANONICAL_EVIDENCE_MODES = {
    "live-source-backed",
    "user-provided sources",
    "illustrative source packet",
    "reasoning-only",
}
EVIDENCE_MODE_RE = re.compile(r"evidence mode\*{0,2}:\*{0,2}\s*`?([^`\n.]+)`?", re.IGNORECASE)
RETRIEVAL_DATE_RE = re.compile(
    r"(?:retrieval date|sources retrieved on)(?:\s*:\s*|\s+\*{0,2})(20\d{2}-\d{2}-\d{2})",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    examples = sorted(path for path in EXAMPLES_DIR.rglob("*.md") if path.name != "README.md")
    if not examples:
        fail("examples/: no markdown examples found")

    for path in examples:
        text = path.read_text(encoding="utf-8")
        lower = text.lower()

        raw_modes = [match.group(1).strip(" *_").lower() for match in EVIDENCE_MODE_RE.finditer(text)]
        if not raw_modes:
            fail(f"{path.relative_to(ROOT)}: missing evidence mode")

        invalid_modes = sorted({mode for mode in raw_modes if mode not in CANONICAL_EVIDENCE_MODES})
        if invalid_modes:
            fail(
                f"{path.relative_to(ROOT)}: non-canonical evidence mode(s): "
                + ", ".join(invalid_modes)
            )

        modes = set(raw_modes)
        if len(modes) != 1:
            fail(f"{path.relative_to(ROOT)}: evidence mode declarations disagree: {sorted(modes)}")

        mode = next(iter(modes))
        if path.name.startswith("live-source-backed-") and mode != "live-source-backed":
            fail(f"{path.relative_to(ROOT)}: live-source-backed filename has mode {mode}")

        if mode == "live-source-backed" and not RETRIEVAL_DATE_RE.search(text):
            fail(f"{path.relative_to(ROOT)}: live-source-backed example missing retrieval date")

        if mode == "reasoning-only" and not (
            "no live sources were checked" in lower
            or "no sources retrieved" in lower
            or "does not cite live sources" in lower
            or "no live verification" in lower
        ):
            fail(f"{path.relative_to(ROOT)}: reasoning-only example must state its source boundary")

        if mode == "illustrative source packet" and not (
            "illustrative" in lower and ("constructed" in lower or "representative" in lower)
        ):
            fail(f"{path.relative_to(ROOT)}: illustrative source packet must identify its constructed evidence")

    print("ok: examples validated")


if __name__ == "__main__":
    main()
