#!/usr/bin/env python3
"""Validate signal archive JSON and markdown consistency."""

from __future__ import annotations

import json
import sys
from pathlib import Path


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
    require_keys(index_path, latest, ("date", "slug", "title", "path", "url"))
    canonical_latest = ROOT / latest["path"]
    if not canonical_latest.exists():
        fail(f"signals/index.json latest path missing: {latest['path']}")

    latest_text = latest_path.read_text(encoding="utf-8")
    if latest["title"] not in latest_text:
        fail("signals/latest.md does not contain the latest title from signals/index.json")
    if latest["path"] not in latest_text:
        fail("signals/latest.md does not contain the latest canonical path from signals/index.json")

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

    print("ok: signal archive validated")


if __name__ == "__main__":
    main()
