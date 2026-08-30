#!/usr/bin/env python3
"""Run all auto-generation scripts."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = (
    ("Sync packaged runtime resources", ["scripts/sync_runtime_resources.py"]),
    ("Auto-sync codex/SKILL.md", ["scripts/build_codex.py"]),
    ("Auto-generate Signal Indexes", ["scripts/build_signals.py"]),
)

def main():
    for label, arguments in BUILDERS:
        print(f"\n== {label} ==", flush=True)
        result = subprocess.run([sys.executable] + arguments, cwd=ROOT)
        if result.returncode:
            print(f"\nFAILED: {label}", file=sys.stderr)
            return result.returncode

    print(f"\nSUCCESS: {len(BUILDERS)} build steps completed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
