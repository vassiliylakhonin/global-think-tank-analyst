# Contributing

Thanks for contributing.

Read [`AGENTS.md`](AGENTS.md) first — it sets the project's identity, honesty rules, evidence rules, and naming hierarchy. Contributions that conflict with those rules will be asked to revise.

## First 15 minutes

If you've just landed in this repo and want to understand it before editing, do these in order. Each step is real-time-boxed at ~5 minutes.

**1. Read these three files, in order:**

1. [`README.md`](README.md) — what this is (horizontal strategic-risk reasoning skill), the four-repo stack, and what the skill is *not* (it is not an agent framework, runtime, MCP server, or eval platform).
2. [`AGENTS.md`](AGENTS.md) — canonical project rules: identity, evidence rules, per-claim provenance tags (Axis A/B), three-value response logic, naming hierarchy, recommended README structure.
3. [`VALIDATION_PLAN.md`](VALIDATION_PLAN.md) — the maturity framework for this repo: practitioner feedback on a small number of reviewable case packets, recorded under [`reviews/`](reviews/). This is deliberately *different* from the vertical-specialist Bar 1 / Bar 2 framework — see `AGENTS.md` "Maturity framework and portfolio canon alignment".

**2. Get the validators running locally:**

```bash
git clone https://github.com/vassiliylakhonin/global-think-tank-analyst
cd global-think-tank-analyst
python3 scripts/validate_signals.py
python3 scripts/validate_json.py
python3 scripts/validate_examples.py
```

Requirements: Python 3.8+. No additional packages — all validators use the standard library. CI hard-stops on all three; run them locally before pushing or `main` will go red.

**3. Read one concrete artifact end-to-end:**

- [`examples/live-source-backed-memo.md`](examples/live-source-backed-memo.md) — the flagship live-source-backed memo (OFAC "Operation Economic Fury" Iran shadow-banking action, 2026-05-01). Paired with [`examples/agenda-projections/live-source-backed-memo.brief.json`](examples/agenda-projections/live-source-backed-memo.brief.json) and `.evidence.json`, this is the smallest complete loop showing how a memo composes with the Agenda Intelligence MD validators.
- For signals: skim [`signals/latest.md`](signals/latest.md) and the [`signals/TEMPLATE.md`](signals/TEMPLATE.md). The 4-file consistency rule across `signals/` is the most common reason a partial signal-add fails CI.

**Unfamiliar with a term in `AGENTS.md`?** See the [portfolio glossary](https://github.com/vassiliylakhonin/agenda-intelligence-md/blob/main/docs/glossary.md) — single source of truth across the four repos for evidence modes, uncertainty labels (`Verified`/`Plausible`/`Judgment`/`Unknown`), Axis A/B provenance tags, three-value response logic, table-cell discipline, and the maturity-framework asymmetry (this repo uses the Maturity framework from `VALIDATION_PLAN.md`; vertical specialists use Bar 1/2; `agenda-intelligence-md` uses `ROADMAP.md` version targets — do not transplant terminology between them).

**When something is unclear**, the lookup order is: this repo's [`AGENTS.md`](AGENTS.md) → portfolio canon ([agenda-intelligence-md/AGENTS.md](https://github.com/vassiliylakhonin/agenda-intelligence-md/blob/main/AGENTS.md), vertical-skill AGENTS.md files) → open an issue using the template under [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/).

---

## Ground rules

- Keep the skill decision-focused and evidence-disciplined.
- Do not add fabricated sources, unsupported certainty, invented metrics, or implied integrations that do not exist.
- Prefer concise, practical improvements over framework bloat.
- Keep agent guidance runtime-neutral unless a section is explicitly for a specific tool.
- When adding examples, make them useful in at least one real user workflow.
- For validation, scoring, schemas, CLI, MCP, or CI tooling, contribute to the companion project [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md) instead.

## Local environment

Requirements: Python 3.8+. No additional packages needed — all validators use the standard library.

Run validators from the repo root:

```bash
python3 scripts/validate_signals.py
python3 scripts/validate_json.py
python3 scripts/validate_examples.py
```

CI hard-stops on all three. Run them before pushing — a red CI on `main` is the only feedback you will get otherwise. See [`scripts/README.md`](scripts/README.md) for what each script checks.

## Development workflow

1. Create a branch from `main`.
2. Edit the relevant files: `SKILL.md`, `codex/SKILL.md`, `AGENTS.md`, `llms.txt`, examples, evals, signals.
3. Run local validators (see above).
4. Keep changes scoped and explain the decision value in the PR.
5. Open a PR with before/after where positioning or behavior changed.

## Where things live

- [`AGENTS.md`](AGENTS.md) — project identity, honesty, evidence, naming rules.
- [`SKILL.md`](SKILL.md) and [`codex/SKILL.md`](codex/SKILL.md) — runtime agent behavior.
- [`examples/`](examples/) — illustrative memos. Always state evidence mode.
- [`evals/`](evals/) — human review checklist, failure modes, starter rubric.
- [`signals/`](signals/) — public examples; contribute via [`signals/TEMPLATE.md`](signals/TEMPLATE.md).
- [`scripts/`](scripts/) — validators and signal generation helper; see [`scripts/README.md`](scripts/README.md).

## Adding a signal

Signals require four files to be updated atomically in the same commit. CI enforces this — a partial update will fail.

1. Create `signals/<slug>.md` from [`signals/TEMPLATE.md`](signals/TEMPLATE.md).
2. Add an entry to `signals/index.json`.
3. Add an entry to `signals/feed.json`.
4. Replace `signals/latest.md` with the new signal.

`python3 scripts/validate_signals.py` checks consistency across all four files.

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
- [ ] All three validators pass locally: `validate_signals.py`, `validate_json.py`, `validate_examples.py`
- [ ] If an example was added or renamed: both `README.md` examples table and `examples/README.md` domain table are updated in the same PR
