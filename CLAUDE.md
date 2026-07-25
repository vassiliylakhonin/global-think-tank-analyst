@AGENTS.md

# Claude Code working rules

`AGENTS.md` is the canonical project contract — apply it, do not restate it. [`SKILL.md`](SKILL.md) is the runtime contract for agents *executing* the skill (memo intake, evidence labels, output modes, self-check).

`AGENTS.md` points to three detail files, loaded when the task needs them:

- [docs/analysis-contract.md](docs/analysis-contract.md) — provenance tags, calibration, response modes, input-claim accounting. Read before producing or reviewing a memo.
- [docs/repo-conventions.md](docs/repo-conventions.md) — README structure, example requirements, eval-doc labelling, signals.
- [docs/maturity-framework.md](docs/maturity-framework.md) — why this repo uses `VALIDATION_PLAN.md` and not the siblings' Bar 1 / Bar 2.

## Validators before push

CI hard-stops on these:

```
python3 scripts/validate_signals.py
python3 scripts/validate_json.py
python3 scripts/validate_examples.py
python3 scripts/validate_codex_sync.py
python3 scripts/check_markdown_links.py
```

`validate_signals.py` enforces the 4-file consistency invariant across `signals/` (index, feed, latest, individual signal) — touching one requires updating the others in the same change.

`validate_codex_sync.py` enforces that the shared analytical contract in `codex/SKILL.md` matches the canonical root `SKILL.md`. Edit `SKILL.md` first, then sync. Deliberate divergences are allowlisted at the top of the script (`CODEX_ONLY_SECTIONS`, `DIVERGENT_SECTIONS`).

## Boundary

Validation, scoring, schemas, CLI, MCP, and CI tooling belong to Agenda Intelligence MD — point there rather than building them here. See AGENTS.md "Relationship to Agenda Intelligence MD".
