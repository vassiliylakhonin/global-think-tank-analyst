@AGENTS.md

# Claude Code working rules

AGENTS.md is the canonical project contract: identity, scope, boundaries, honesty rules, evidence rules, provenance tags, three-value response logic, naming, portfolio relationships. Follow it. Do not re-derive or restate those rules — apply them.

SKILL.md is the runtime contract for agents executing the skill (memo intake, evidence labels, output modes, self-check).

This file (CLAUDE.md) contains only Claude-Code-specific working rules for this repo, on top of the global ~/.claude/CLAUDE.md.

## Project-specific paths to inspect

In addition to the global pre-edit checklist, scan these when relevant:
- SKILL.md
- llms.txt
- examples/
- docs/
- signals/
- evals/
- scripts/

## Validators before push

CI hard-stops on these — run them locally before pushing or PR will go red on main:

```
python3 scripts/validate_signals.py
python3 scripts/validate_json.py
python3 scripts/validate_examples.py
python3 scripts/validate_codex_sync.py
```

`validate_signals.py` enforces the 4-file consistency invariant across signals/ (index, feed, latest, individual signal). Touching any one of those four requires updating the others in the same change.

`validate_codex_sync.py` enforces that the shared analytical contract in `codex/SKILL.md` matches the canonical root `SKILL.md`. When changing core behavior, edit `SKILL.md` first, then sync the shared section into `codex/SKILL.md`. Intentional codex-only or divergent sections are allowlisted at the top of the script (`CODEX_ONLY_SECTIONS`, `DIVERGENT_SECTIONS`); add a header there if a divergence is deliberate.

## Working style in this repo

Small, reviewable changes. Do not rewrite the project unless I explicitly ask.

If validation, scoring, schemas, CLI, MCP, or CI checks come up: present them as possible future work only when explicitly requested, or point to Agenda Intelligence MD if the appropriate companion already documents them. See AGENTS.md "Relationship to Agenda Intelligence MD".
