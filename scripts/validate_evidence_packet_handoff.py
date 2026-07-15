#!/usr/bin/env python3
"""Validate the repository's Agenda Intelligence evidence-packet handoff."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "examples/evidence-packet-handoff.json"
REQUIRED_DOCS = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "docs/evidence-packet-handoff.md"]
REQUIRED_PHRASES = [
    "deterministic evidence-packet linter",
    "packet completeness",
    "not factual truth",
    "examples/evidence-packet-handoff.json",
]
STALE_PRIMARY_POSITIONING = [
    "commercial product shell",
    "current product focus is evidence-readiness / trust-routing",
    "first discovery wedge",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_docs() -> None:
    for path in REQUIRED_DOCS:
        if not path.exists():
            fail(f"missing required handoff documentation: {path.relative_to(ROOT)}")

    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in REQUIRED_DOCS)
    for phrase in REQUIRED_PHRASES:
        if phrase.lower() not in combined:
            fail(f"handoff documentation missing phrase: {phrase}")

    core = "\n".join(
        (ROOT / name).read_text(encoding="utf-8").lower()
        for name in ("README.md", "AGENTS.md", "CONTEXT.md", "llms.txt")
    )
    for phrase in STALE_PRIMARY_POSITIONING:
        if phrase in core:
            fail(f"stale primary positioning remains in core docs: {phrase}")


def validate_packet() -> None:
    try:
        packet = json.loads(PACKET.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing packet example: {PACKET.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"invalid packet JSON: {exc}")

    if not isinstance(packet, dict):
        fail("packet must be a JSON object")
    if not isinstance(packet.get("claims"), list) or not packet["claims"]:
        fail("packet claims must be a non-empty array")
    if not isinstance(packet.get("sources"), list):
        fail("packet sources must be an array")

    sources: dict[str, str] = {}
    for source in packet["sources"]:
        if not isinstance(source, dict):
            fail("each source must be an object")
        source_id = source.get("source_id")
        source_text = source.get("text")
        if not nonempty_string(source_id) or not nonempty_string(source_text):
            fail("each source requires non-empty source_id and text")
        if source_id in sources:
            fail(f"duplicate source_id: {source_id}")
        sources[source_id] = source_text

    claim_ids: set[str] = set()
    for claim in packet["claims"]:
        if not isinstance(claim, dict):
            fail("each claim must be an object")
        claim_id = claim.get("claim_id")
        if not nonempty_string(claim_id) or not nonempty_string(claim.get("text")):
            fail("each claim requires non-empty claim_id and text")
        if claim_id in claim_ids:
            fail(f"duplicate claim_id: {claim_id}")
        claim_ids.add(claim_id)

        source_ids = claim.get("source_ids", [])
        if not isinstance(source_ids, list) or len(source_ids) != len(set(source_ids)):
            fail(f"{claim_id}: source_ids must be a unique array")
        for source_id in source_ids:
            if source_id not in sources:
                fail(f"{claim_id}: unresolved source_id: {source_id}")

        for quote in claim.get("quotes", []):
            if not isinstance(quote, dict):
                fail(f"{claim_id}: each quote must be an object")
            source_id = quote.get("source_id")
            text = quote.get("text")
            if source_id not in source_ids:
                fail(f"{claim_id}: quote source must also be declared in source_ids")
            if not nonempty_string(text) or text not in sources[source_id]:
                fail(f"{claim_id}: quote must be a verbatim span in its source text")


def main() -> None:
    validate_docs()
    validate_packet()
    print("ok: evidence-packet handoff validated")


if __name__ == "__main__":
    main()
