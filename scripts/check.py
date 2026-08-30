#!/usr/bin/env python3
"""Run every supported repository check through one interface."""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    ("skill package", ("scripts/validate_skill_package.py",)),
    ("runtime skill resources", ("scripts/validate_runtime_resources.py",)),
    ("repository JSON", ("scripts/validate_json.py",)),
    # ("signal archive", ("scripts/validate_signals.py",)), # Deprecated: now auto-generated
    ("signal pipeline tests", ("scripts/test_signal_pipeline.py",)),
    ("evidence-packet handoff", ("scripts/validate_evidence_packet_handoff.py",)),
    ("example evidence discipline", ("scripts/validate_examples.py",)),
    # ("Codex variant sync", ("scripts/validate_codex_sync.py",)), # Deprecated: now auto-generated
    (
        "skill-improvement cases",
        (
            "evals/skill-improvement/tools/validate_cases.py",
            "evals/skill-improvement/cases/global-think-tank-analyst.jsonl",
        ),
    ),
    ("Markdown links", ("scripts/check_markdown_links.py",)),
)


def main():
    for label, arguments in CHECKS:
        print(f"\n== {label} ==", flush=True)
        result = subprocess.run((sys.executable, *arguments), cwd=ROOT)
        if result.returncode:
            print(f"\nFAILED: {label}", file=sys.stderr)
            return result.returncode

    print(f"\nPASS: {len(CHECKS)} repository checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
