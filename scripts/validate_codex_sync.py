#!/usr/bin/env python3
"""Guard: codex/SKILL.md shared sections must stay in sync with canonical root SKILL.md.

codex/SKILL.md is intentionally self-contained (it may be loaded without SKILL.md)
and copies the shared analytical contract from the canonical root SKILL.md. Its own
"Contract provenance" section asks the author to sync the shared sections by hand.
This check enforces that discipline instead of relying on memory: it fails the build
when a shared section drifts.

Two allowlists encode intentional divergence:
  - CODEX_ONLY_SECTIONS:  sections that exist only in codex (platform-specific).
  - DIVERGENT_SECTIONS:   shared section headers whose body is expected to differ.

Anything else is a failure: a root section missing from codex, a shared-section body
that differs without being allowlisted, or an undeclared codex-only section.

Usage:
  python3 scripts/validate_codex_sync.py [root_path codex_path]
(paths default to SKILL.md and codex/SKILL.md; optional args exist for testing.)
"""
import re
import sys

CODEX_ONLY_SECTIONS = {
    "Contract provenance",
    "Codex Platform Setup",
    "JSON Output Mode",
    "Pipeline Integration with Agenda Intelligence MD",
}

# Shared sections that legitimately differ between root and codex.
DIVERGENT_SECTIONS = {
    "Mode F — Analyst Training",     # codex adds an agentic-loop escalation note
    "Installation and integration",  # codex-specific install paths and relative links
}


def sections(path):
    """Return {header_text: body} for ## / ### headers, ignoring fenced code blocks."""
    secs = {}
    cur = None
    buf = []
    in_fence = False
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                if cur is not None:
                    buf.append(line)
                continue
            m = re.match(r"^(#{2,3}) (.+)$", line)
            if m and not in_fence:
                if cur is not None:
                    secs[cur] = "\n".join(buf).strip()
                cur = m.group(2).strip()
                buf = []
            elif cur is not None:
                buf.append(line)
    if cur is not None:
        secs[cur] = "\n".join(buf).strip()
    return secs


def main():
    root_path = sys.argv[1] if len(sys.argv) > 2 else "SKILL.md"
    codex_path = sys.argv[2] if len(sys.argv) > 2 else "codex/SKILL.md"

    root = sections(root_path)
    codex = sections(codex_path)
    errors = []

    for name, body in root.items():
        if name not in codex:
            errors.append(f"MISSING in {codex_path}: shared section '{name}' (present in {root_path})")
            continue
        if name in DIVERGENT_SECTIONS:
            continue
        if body != codex[name]:
            errors.append(f"DRIFT in shared section '{name}': body differs from canonical {root_path}")

    for name in codex:
        if name not in root and name not in CODEX_ONLY_SECTIONS and name not in DIVERGENT_SECTIONS:
            errors.append(
                f"UNDECLARED codex-only section '{name}' in {codex_path}: "
                f"add it to CODEX_ONLY_SECTIONS in this script if it is intentional"
            )

    if errors:
        print(f"codex/SKILL.md is out of sync with canonical root {root_path}:\n")
        for e in errors:
            print(f"  - {e}")
        print(f"\nFix: update {root_path} first (canonical), then sync the shared section into {codex_path}.")
        print("If a divergence is intentional, add the header to DIVERGENT_SECTIONS or "
              "CODEX_ONLY_SECTIONS in scripts/validate_codex_sync.py.")
        sys.exit(1)

    print(
        f"ok: codex/SKILL.md shared sections in sync with {root_path} "
        f"({len(root)} root sections; {len(DIVERGENT_SECTIONS)} allowed-divergent, "
        f"{len(CODEX_ONLY_SECTIONS)} codex-only)"
    )


if __name__ == "__main__":
    main()
