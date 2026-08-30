# Contributing

Thanks for contributing.

Read [`AGENTS.md`](AGENTS.md) first — it sets the project's identity, honesty rules, evidence rules, and naming hierarchy. Contributions that conflict with those rules will be asked to revise.

## First 15 minutes

If you've just landed in this repo and want to understand it before editing, do these in order. Each step is real-time-boxed at ~5 minutes.

**1. Read these three files, in order:**

1. [`README.md`](README.md) — what this is (a horizontal strategic-risk reasoning skill with a small developer toolkit), the four-repo stack, and which runtime surfaces are explicitly experimental.
2. [`AGENTS.md`](AGENTS.md) — canonical project rules: identity, honesty rules, evidence rules, retrieved-content trust, naming hierarchy. It points to [`docs/analysis-contract.md`](docs/analysis-contract.md) (provenance tags, calibration, response modes), [`docs/repo-conventions.md`](docs/repo-conventions.md) (README, examples, eval docs, signals), and [`docs/maturity-framework.md`](docs/maturity-framework.md).
3. [`VALIDATION_PLAN.md`](VALIDATION_PLAN.md) — the maturity framework for this repo: practitioner feedback on a small number of reviewable case packets, recorded under [`reviews/`](reviews/). This is deliberately *different* from the vertical-specialist Bar 1 / Bar 2 framework — see [`docs/maturity-framework.md`](docs/maturity-framework.md).

**2. Get the validators running locally:**

```bash
git clone https://github.com/vassiliylakhonin/global-think-tank-analyst
cd global-think-tank-analyst
python3 scripts/check.py
```

Requirements: Python 3.8+ for the dependency-free repository validators. The
installable Python package requires Python 3.10+. CI runs the same repository
checks and then smoke-tests a built wheel.

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
- For evidence-packet linting or changes to its contract, contribute to the companion project [Agenda Intelligence MD](https://github.com/vassiliylakhonin/agenda-intelligence-md) instead. Older memo validation, scoring, and MCP contracts remain owned there as compatibility surfaces.

## Local environment

Requirements: Python 3.8+ for these dependency-free validators. Package and
runtime development requires Python 3.10+.

Run validators from the repo root:

```bash
python3 scripts/check.py
```

The runner stops on the first failure. See [`scripts/README.md`](scripts/README.md) for what each script checks.

## Development workflow

1. Create a branch from `main`.
2. Edit the relevant files: `SKILL.md`, `codex/SKILL.md`, `AGENTS.md`, `llms.txt`, examples, evals, signals.
3. Run local validators (see above).
4. For package changes, build and smoke-test the installed artifact:
   `python -m pip install -e ".[test,mcp]"`, then
   `python -m build --wheel && python scripts/test_wheel_install.py`.
5. Keep changes scoped and explain the decision value in the PR.
6. Open a PR with before/after where positioning or behavior changed.

Release publication uses PyPI Trusted Publishing. Follow
[`docs/publishing.md`](docs/publishing.md); do not add a PyPI token to the
repository.

## Where things live

- [`AGENTS.md`](AGENTS.md) — project identity, honesty, evidence, naming rules. The contract, kept short.
- [`docs/analysis-contract.md`](docs/analysis-contract.md) — provenance tags, calibration, response modes, input-claim accounting.
- [`docs/repo-conventions.md`](docs/repo-conventions.md) — README structure, example requirements, eval-doc labelling, signals.
- [`docs/maturity-framework.md`](docs/maturity-framework.md) — why this repo uses `VALIDATION_PLAN.md` and not Bar 1/2.

**Where a new rule goes.** `AGENTS.md` stays short; task-specific detail lives in the three files above and is reached from it by a pointer — see AGENTS.md "Where a new rule goes". A rule belongs inline only if it is needed before any output. Adding a section to `AGENTS.md` when one of the `docs/` files owns it is the drift this layout exists to prevent.
- [`SKILL.md`](SKILL.md) and [`codex/SKILL.md`](codex/SKILL.md) — runtime agent behavior.
- [`examples/`](examples/) — illustrative memos. Always state evidence mode.
- [`evals/`](evals/) — human review checklist, failure modes, starter rubric.
- [`signals/`](signals/) — public examples; contribute via [`signals/TEMPLATE.md`](signals/TEMPLATE.md).
- [`scripts/`](scripts/) — validators and signal generation helper; see [`scripts/README.md`](scripts/README.md).

## Adding a signal

The manual process of updating JSON files has been deprecated in favor of automation.

1. Create `signals/<slug>.md` from [`signals/TEMPLATE.md`](signals/TEMPLATE.md).
2. Commit your markdown file.
3. The automated CI/CD pipeline (or build script) will handle indexing this signal into `index.json`, `feed.json`, and `latest.md`.

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

- [ ] Packaged `SKILL.md` discovery fields pass `scripts/validate_skill_package.py`
- [ ] Behavior or positioning change is documented in `CHANGELOG.md`
- [ ] Examples state evidence mode and do not fabricate citations
- [ ] No exaggerated language ("revolutionary", "production-grade", "guarantees correctness", "fully autonomous")
- [ ] `python3 scripts/check.py` passes locally
- [ ] Package changes pass `python -m build --wheel && python scripts/test_wheel_install.py` in an environment with `.[test,mcp]`
- [ ] If an example was added or renamed, update the master table in `examples/README.md` (the root README table will be synced automatically).
- [ ] Note: Manual syncing of `codex/SKILL.md` is no longer required; it will be generated automatically by the build pipeline.
