#!/usr/bin/env python3
"""Validate repository-owned skill packaging invariants.

This check guards the discovery fields and canonical-file relationships used by
this repository. It is intentionally narrower than the complete Agent Skills
and Agent Plugins schemas; it does not claim full specification conformance.
"""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "global-think-tank-analyst"
SKILL_FILE = SKILL_DIR / "SKILL.md"
CANONICAL_SKILL = ROOT / "SKILL.md"
MANIFESTS = (
    ROOT / "plugin.json",
    ROOT / ".claude-plugin" / "plugin.json",
)
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def frontmatter_scalar(path, key):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)}: frontmatter opening delimiter missing")

    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"{path.relative_to(ROOT)}: frontmatter closing delimiter missing")

    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text[4:end], re.MULTILINE)
    if not match:
        fail(f"{path.relative_to(ROOT)}: {key!r} missing from frontmatter")
    return match.group(1)


def validate_skill():
    if not SKILL_FILE.is_symlink():
        fail(f"{SKILL_FILE.relative_to(ROOT)} must remain a symlink to canonical SKILL.md")

    try:
        resolved_skill = SKILL_FILE.resolve(strict=True)
    except OSError as exc:
        fail(f"cannot resolve {SKILL_FILE.relative_to(ROOT)}: {exc}")

    if resolved_skill != CANONICAL_SKILL.resolve(strict=True):
        fail(f"{SKILL_FILE.relative_to(ROOT)} must resolve to canonical SKILL.md")

    name = frontmatter_scalar(SKILL_FILE, "name")
    description = frontmatter_scalar(SKILL_FILE, "description")

    if not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        fail("skill name must contain at most 64 lowercase letters, digits, and single hyphens")
    if name != SKILL_DIR.name:
        fail(f"skill name {name!r} must match parent directory {SKILL_DIR.name!r}")
    if not 1 <= len(description) <= 1024:
        fail("skill description must contain between 1 and 1024 characters")


def validate_manifests():
    documents = []
    for path in MANIFESTS:
        try:
            documents.append((path, json.loads(path.read_text(encoding="utf-8"))))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"cannot read {path.relative_to(ROOT)}: {exc}")

    root_manifest = documents[0][1]
    if root_manifest.get("name") != SKILL_DIR.name:
        fail("plugin.json name must match the packaged skill directory")

    shared_fields = ("name", "version", "description", "author", "homepage", "license", "keywords")
    for field in shared_fields:
        values = [document.get(field) for _, document in documents]
        if values[0] != values[1]:
            fail(f"plugin manifests disagree on {field!r}")


def main():
    validate_skill()
    validate_manifests()
    print("ok: skill discovery fields, canonical symlink, and plugin manifests are consistent")


if __name__ == "__main__":
    main()
