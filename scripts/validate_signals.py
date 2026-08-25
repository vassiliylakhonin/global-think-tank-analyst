#!/usr/bin/env python3
"""Validate signal archive JSON and markdown consistency."""

from __future__ import annotations

import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

import generate_policy_risk_signal as generator  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SIGNALS_DIR = ROOT / "signals"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict:
    if not path.exists():
        fail(f"{path.relative_to(ROOT)} missing")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} invalid JSON: {exc}")


def require_keys(path: Path, payload: dict, keys: tuple[str, ...]) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        fail(f"{path.relative_to(ROOT)} missing keys: {missing}")


def check_archive_readme() -> None:
    """signals/README.md is rewritten by the generator; the two must agree.

    The generator owns the prose around the signal list. When its constants
    drifted from the file, every run silently reverted the documented
    same-day filename convention.
    """
    readme_path = SIGNALS_DIR / "README.md"
    if not readme_path.exists():
        fail("signals/README.md missing")
    readme = readme_path.read_text(encoding="utf-8")
    if not readme.startswith(generator.ARCHIVE_HEADER):
        fail(
            "signals/README.md header differs from ARCHIVE_HEADER in "
            "scripts/generate_policy_risk_signal.py; edit both together"
        )
    if not readme.endswith(generator.ARCHIVE_FOOTER):
        fail(
            "signals/README.md footer differs from ARCHIVE_FOOTER in "
            "scripts/generate_policy_risk_signal.py; edit both together"
        )


def main() -> None:
    index_path = SIGNALS_DIR / "index.json"
    feed_path = SIGNALS_DIR / "feed.json"
    latest_path = SIGNALS_DIR / "latest.md"

    index = load_json(index_path)
    feed = load_json(feed_path)

    require_keys(index_path, index, ("title", "description", "latest", "signals"))
    require_keys(feed_path, feed, ("version", "title", "home_page_url", "feed_url", "items"))

    if not isinstance(index["signals"], list):
        fail("signals/index.json: signals must be a list")
    if not isinstance(feed["items"], list):
        fail("signals/feed.json: items must be a list")

    latest = index["latest"]
    if not isinstance(latest, dict):
        fail("signals/index.json: latest must be an object")
    require_keys(index_path, latest, ("date", "slug", "title", "path", "url"))
    canonical_latest = ROOT / latest["path"]
    if not canonical_latest.exists():
        fail(f"signals/index.json latest path missing: {latest['path']}")

    if index["signals"]:
        newest = max(index["signals"], key=lambda s: s["date"])
        if newest["slug"] != latest["slug"]:
            fail(
                f"signals/index.json 'latest' is '{latest['slug']}' "
                f"but newest signal by date is '{newest['slug']}' ({newest['date']})"
            )

    if not latest_path.exists():
        fail("signals/latest.md missing")
    latest_text = latest_path.read_text(encoding="utf-8")
    if latest["title"] not in latest_text:
        fail("signals/latest.md does not contain the latest title from signals/index.json")
    if latest["path"] not in latest_text:
        fail("signals/latest.md does not contain the latest canonical path from signals/index.json")

    for position, item in enumerate(feed["items"]):
        if not isinstance(item, dict):
            fail(f"signals/feed.json: items[{position}] must be an object")
    feed_by_url = {item.get("url"): item for item in feed["items"]}

    for signal in index["signals"]:
        require_keys(index_path, signal, ("date", "slug", "title", "path", "url"))

        markdown_path = ROOT / signal["path"]
        if not markdown_path.exists():
            fail(f"signals/index.json path missing: {signal['path']}")

        markdown = markdown_path.read_text(encoding="utf-8")
        if signal["title"] not in markdown:
            fail(f"{signal['path']}: markdown does not contain index title")
        if f"Date: {signal['date']}" not in markdown:
            fail(f"{signal['path']}: markdown does not contain index date")

        feed_item = feed_by_url.get(signal["url"])
        if not feed_item:
            fail(f"signals/feed.json missing URL from index: {signal['url']}")

        expected_title = f"{signal['date']}: {signal['title']}"
        expected_date = f"{signal['date']}T00:00:00Z"

        if feed_item.get("id") != signal["url"]:
            fail(f"signals/feed.json id mismatch for {signal['slug']}")
        if feed_item.get("title") != expected_title:
            fail(f"signals/feed.json title mismatch for {signal['slug']}")
        if feed_item.get("date_published") != expected_date:
            fail(f"signals/feed.json date mismatch for {signal['slug']}")
        if signal["title"] not in feed_item.get("content_text", ""):
            fail(f"signals/feed.json content missing title for {signal['slug']}")

    check_archive_readme()

    print("ok: signal archive validated")


if __name__ == "__main__":
    main()
