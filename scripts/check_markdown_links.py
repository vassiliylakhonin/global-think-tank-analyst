#!/usr/bin/env python3
"""Fail when a tracked Markdown file points at a missing local path.

Also fails when a link to the author's own site returns 404/410, because those
URLs move when the site is restructured and nothing else catches them. Network
errors and other statuses are reported but never fail the run, so CI stays
deterministic when the network is unavailable. Set SKIP_SITE_LINK_CHECK=1 to
skip the network step entirely.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*(?:```|~~~)")
OWN_SITE_PREFIX = "https://vassiliylakhonin.github.io"
GONE_STATUSES = {404, 410}
REQUEST_TIMEOUT = 10


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


def own_site_target(raw_target: str) -> str | None:
    target = raw_target.strip().strip("<>")
    if " " in target:
        target = target.split(" ", 1)[0]
    if not target.startswith(OWN_SITE_PREFIX):
        return None
    return target.split("#", 1)[0]


def site_link_status(url: str) -> tuple[int | None, str | None]:
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            return response.status, None
    except urllib.error.HTTPError as error:
        return error.code, None
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return None, str(error)


def check_own_site_links(urls: dict[str, list[str]]) -> tuple[list[str], list[str]]:
    gone: list[str] = []
    unchecked: list[str] = []
    for url in sorted(urls):
        status, error = site_link_status(url)
        locations = ", ".join(urls[url])
        if status in GONE_STATUSES:
            gone.append(f"{url} -> HTTP {status} ({locations})")
        elif status is None:
            unchecked.append(f"{url} -> not checked: {error}")
    return gone, unchecked


def main() -> int:
    missing: list[str] = []
    site_links: dict[str, list[str]] = {}
    for markdown in tracked_markdown_files():
        text = markdown.read_text(encoding="utf-8")
        in_fence = False
        for line_number, line in enumerate(text.splitlines(), 1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for raw_target in LINK_RE.findall(line):
                site_url = own_site_target(raw_target)
                if site_url is not None:
                    site_links.setdefault(site_url, []).append(
                        f"{markdown.relative_to(ROOT)}:{line_number}"
                    )
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

    if os.environ.get("SKIP_SITE_LINK_CHECK") == "1":
        print("skipped: own-site link check (SKIP_SITE_LINK_CHECK=1)")
        return 0

    gone, unchecked = check_own_site_links(site_links)
    for item in unchecked:
        print(f"warning: {item}")
    if gone:
        print("Dead links to the author's own site:")
        print("\n".join(f"  {item}" for item in gone))
        return 1

    print(f"ok: {len(site_links)} own-site link(s) resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
