#!/usr/bin/env python3
"""Validate that repository JSON files parse cleanly."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts)


def main() -> None:
    json_files = sorted(path for path in ROOT.rglob("*.json") if not is_skipped(path))
    if not json_files:
        fail("no JSON files found")

    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{path.relative_to(ROOT)} invalid JSON: {exc}")

    print(f"ok: {len(json_files)} JSON files validated")


if __name__ == "__main__":
    main()
