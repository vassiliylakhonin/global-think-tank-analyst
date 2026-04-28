#!/usr/bin/env python3
"""Generate a weekly Policy Risk Signal draft from public RSS/Atom sources.

The script is designed for GitHub Actions. It fetches public source snippets,
asks an LLM to choose one decision-relevant signal, writes a dated markdown file,
and updates the signal archive/README index. It opens a PR via workflow rather
than publishing directly to main.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / ".github" / "policy-risk-signal" / "sources.json"
SIGNALS_DIR = ROOT / "signals"
README_PATH = ROOT / "README.md"
ARCHIVE_PATH = SIGNALS_DIR / "README.md"

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SYSTEM_PROMPT = """You generate one weekly Policy Risk Signal for a public GitHub repository.

Audience: analysts, founders, operators, compliance/risk teams, and policy-curious builders evaluating a policy-risk memo skill.

Hard rules:
- Use only the provided source snippets and URLs.
- Do not invent facts, numbers, policy changes, citations, URLs, dates, or causal claims.
- If evidence is thin, say so clearly.
- Pick one signal that can support a short decision-relevant analysis.
- Write concise markdown only, no code fences.
- Keep it sober, useful, and non-sensational.
- This is decision-support content, not legal/compliance/investment advice.
"""

USER_TEMPLATE = """Date: {date}

Repository: Policy Risk Memo Architect — a skill for decision-ready geopolitical, sanctions, trade, regulatory, and strategic-risk memos.

Task: Create one short weekly Policy Risk Signal from the source snippets below.

Required markdown format:
# Policy Risk Signal — {date}

## Signal
One short paragraph explaining what public signal is visible from the provided sources.

## Why it matters
2-3 bullets focused on decision relevance.

## Decision question
One concrete question this should trigger for a company, investor, NGO, analyst, or policy team.

## Quick assessment
- **Fact:** one source-backed fact from snippets.
- **Assessment:** one bounded judgment.
- **Unknown:** one material unknown.
- **Main risk:** one practical risk.

## What to watch
- 3 observable indicators.

## Sources
- [Source title](URL) — source name

## Example expansion prompt
A short prompt that asks Policy Risk Memo Architect to expand the signal into a standard memo.

Source snippets:
{snippets}
"""


def strip_text(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    value = re.sub(r"\s+", " ", value).strip()
    return value


def fetch_url(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "policy-risk-signal-bot/1.0 (+https://github.com/vassiliylakhonin/global-think-tank-analyst)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def parse_feed(raw: bytes, base_url: str, limit: int = 5) -> list[dict[str, str]]:
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []

    items: list[dict[str, str]] = []

    # RSS
    for item in root.findall(".//item")[:limit]:
        title = strip_text(item.findtext("title") or "")
        link = strip_text(item.findtext("link") or "")
        description = strip_text(item.findtext("description") or item.findtext("summary") or "")
        date = strip_text(item.findtext("pubDate") or item.findtext("date") or "")
        if title and link:
            items.append({"title": title, "url": link, "summary": description[:500], "date": date})

    # Atom fallback
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall(".//atom:entry", ns)[:limit]:
        title = strip_text(entry.findtext("atom:title", default="", namespaces=ns))
        link = ""
        for link_el in entry.findall("atom:link", ns):
            href = link_el.attrib.get("href")
            if href:
                link = urllib.parse.urljoin(base_url, href)
                break
        summary = strip_text(entry.findtext("atom:summary", default="", namespaces=ns) or entry.findtext("atom:content", default="", namespaces=ns))
        date = strip_text(entry.findtext("atom:updated", default="", namespaces=ns) or entry.findtext("atom:published", default="", namespaces=ns))
        if title and link:
            items.append({"title": title, "url": link, "summary": summary[:500], "date": date})

    return items[:limit]


def collect_snippets(limit_per_source: int = 4) -> str:
    config = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    blocks: list[str] = []
    errors: list[str] = []
    for source in config.get("sources", []):
        name = source["name"]
        url = source["url"]
        try:
            raw = fetch_url(url)
            items = parse_feed(raw, url, limit=limit_per_source)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            errors.append(f"- {name}: fetch failed ({exc})")
            continue
        if not items:
            errors.append(f"- {name}: no parseable feed items")
            continue
        lines = [f"SOURCE: {name}", f"FOCUS: {source.get('focus', '')}", f"FEED: {url}"]
        for item in items:
            lines.append(f"- TITLE: {item['title']}\n  URL: {item['url']}\n  DATE: {item.get('date', '')}\n  SUMMARY: {item.get('summary', '')}")
        blocks.append("\n".join(lines))
    if errors:
        blocks.append("SOURCE FETCH NOTES:\n" + "\n".join(errors))
    if not blocks:
        raise SystemExit("No source snippets collected")
    return "\n\n---\n\n".join(blocks)


def openai_generate(prompt: str, model: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is required for full automatic signal generation")
    payload: dict[str, Any] = {
        "model": model,
        "input": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_output_tokens": 1400,
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenAI API error {exc.code}: {body[:1000]}") from exc

    chunks: list[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                chunks.append(content.get("text", ""))
    text = "\n".join(chunks).strip()
    if not text:
        raise SystemExit("OpenAI response did not contain output text")
    return text


def signal_title(markdown: str) -> str:
    for line in markdown.splitlines():
        if line.startswith("## Signal"):
            continue
        if line.startswith("# "):
            continue
    match = re.search(r"## Signal\s+(.+?)(?:\n## |\Z)", markdown, re.S)
    if match:
        paragraph = strip_text(match.group(1)).split(".")[0]
        return paragraph[:110].rstrip() or "weekly policy risk signal"
    return "weekly policy risk signal"


def update_archive(date: str, rel_path: str, title: str) -> None:
    archive = f"""# Policy Risk Signals

Short, source-aware policy risk notes showing how Policy Risk Memo Architect turns public signals into decision-ready analysis.

Each signal is intentionally brief: one public signal, why it matters, one decision question, a bounded assessment, and indicators to watch.

## Latest signals

"""
    existing: list[str] = []
    if ARCHIVE_PATH.exists():
        text = ARCHIVE_PATH.read_text(encoding="utf-8")
        existing = [line for line in text.splitlines() if line.startswith("- [")]
    new_line = f"- [{date}]({rel_path}): {title}"
    lines = [new_line] + [line for line in existing if f"]({rel_path})" not in line]
    archive += "\n".join(lines[:20]) + "\n"
    ARCHIVE_PATH.write_text(archive, encoding="utf-8")


def update_main_readme(date: str, rel_path: str, title: str) -> None:
    text = README_PATH.read_text(encoding="utf-8")
    block = f"""## Policy Risk Signal — 7 days of signals → decision memos

Short, source-aware policy risk notes showing how this skill turns public signals into decision-ready analysis.

- [{date}]({rel_path}): {title}

[Full signal archive →](signals)

"""
    start = text.find("## Policy Risk Signal — 7 days of signals → decision memos")
    if start != -1:
        next_heading = text.find("\n## ", start + 1)
        if next_heading == -1:
            text = text[:start] + block.rstrip() + "\n"
        else:
            text = text[:start] + block + text[next_heading + 1 :]
    else:
        marker = "## Installation\n"
        if marker not in text:
            raise SystemExit("README insertion marker not found")
        text = text.replace(marker, block + marker, 1)
    README_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    date = args.date
    year = date[:4]
    snippets = collect_snippets()
    prompt = USER_TEMPLATE.format(date=date, snippets=snippets)
    markdown = openai_generate(prompt, args.model)
    if "## Sources" not in markdown or "## Quick assessment" not in markdown:
        raise SystemExit("Generated signal is missing required sections")

    out_dir = SIGNALS_DIR / year
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{date}.md"
    rel_path = out_path.relative_to(ROOT).as_posix()
    title = signal_title(markdown)

    if args.dry_run:
        print(markdown)
        return

    out_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    update_archive(date, rel_path, title)
    update_main_readme(date, rel_path, title)
    print(f"Wrote {rel_path}")


if __name__ == "__main__":
    main()
