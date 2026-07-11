#!/usr/bin/env python3
"""Fail when a tracked Markdown file points at a missing local path."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def tracked_markdown_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "*.md"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / path.decode() for path in result.stdout.split(b"\0") if path]


def local_target(raw_target: str) -> str | None:
    target = raw_target.strip().strip("<>")
    if not target:
        return None
    if " " in target and not target.startswith(("./", "../", "/")):
        target = target.split(" ", 1)[0]
    if target.startswith(("#", "http://", "https://", "mailto:", "tel:")):
        return None
    target = unquote(target.split("#", 1)[0])
    if not target or target == "URL":
        return None
    return target


def main() -> int:
    missing: list[str] = []
    for markdown in tracked_markdown_files():
        text = markdown.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), 1):
            for raw_target in LINK_RE.findall(line):
                target = local_target(raw_target)
                if target is None:
                    continue
                resolved = (ROOT / target.lstrip("/")) if target.startswith("/") else (markdown.parent / target)
                if not resolved.exists():
                    missing.append(f"{markdown.relative_to(ROOT)}:{line_number}: {raw_target}")

    if missing:
        print("Broken local Markdown links:")
        print("\n".join(f"  {item}" for item in missing))
        return 1

    print("ok: tracked Markdown links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
