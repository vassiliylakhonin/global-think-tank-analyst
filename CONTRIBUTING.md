# Contributing

Thanks for contributing.

Read [`AGENTS.md`](AGENTS.md) first — it sets the project's identity, honesty rules, evidence rules, and naming hierarchy. Contributions that conflict with those rules will be asked to revise.

## Ground rules

- Keep the skill decision-focused and evidence-disciplined.
- Do not add fabricated sources, unsupported certainty, invented metrics, or implied integrations that do not exist.
- Prefer concise, practical improvements over framework bloat.
- Keep agent guidance runtime-neutral unless a section is explicitly for a specific tool.
- When adding examples, make them useful in at least one real user workflow.
- For validation, scoring, schemas, CLI, MCP, or CI tooling, contribute to the companion project [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md) instead.

## Development workflow

1. Create a branch from `main`.
2. Edit the relevant files: `SKILL.md`, `codex/SKILL.md`, `AGENTS.md`, `llms.txt`, examples, evals, signals.
3. Keep changes scoped and explain the decision value in the PR.
4. Open a PR with before/after where positioning or behavior changed.

## Where things live

- [`AGENTS.md`](AGENTS.md) — project identity, honesty, evidence, naming rules.
- [`SKILL.md`](SKILL.md) and [`codex/SKILL.md`](codex/SKILL.md) — runtime agent behavior.
- [`examples/`](examples/) — illustrative memos. Always state evidence mode.
- [`evals/`](evals/) — human review checklist, failure modes, starter rubric.
- [`signals/`](signals/) — public examples; contribute via [`signals/TEMPLATE.md`](signals/TEMPLATE.md).

## Examples must include

- user question
- evidence mode (`live-source-backed`, `user-provided sources`, `illustrative source packet`, or `reasoning-only`)
- decision context, key judgment
- facts vs assessments, assumptions, uncertainty
- actor incentives / leverage
- scenarios, options / trade-offs
- watch-next indicators, confidence
- what would change the judgment

## PR checklist

- [ ] `name` and `description` remain valid in `SKILL.md` and `codex/SKILL.md` frontmatter
- [ ] Behavior or positioning change is documented in `CHANGELOG.md` (under `Unreleased` or a new version)
- [ ] `AGENTS.md`, `SKILL.md`, `codex/SKILL.md`, `llms.txt`, and `README.md` remain aligned
- [ ] Naming hierarchy preserved: Product = Global Think Tank Analyst; Method = Policy Risk Memo Architect; Companion = Agenda Intelligence MD
- [ ] Examples state evidence mode and do not fabricate citations
- [ ] No claims of external verification, validation, MCP, CLI, or CI checks unless truly implemented in this repo
- [ ] No exaggerated language ("revolutionary", "production-grade", "guarantees correctness", "fully autonomous")
