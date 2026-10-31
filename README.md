# Global Think Tank Analyst

A reasoning skill and Python toolkit for turning a policy or geopolitical question into a structured decision memo with explicit evidence, alternatives, uncertainty, and review requirements.

Use it when a general AI answer is too difficult to audit: a market-entry decision, regulatory exposure, disrupted trade corridor, or competing policy scenarios. The method forces the model to separate facts, assumptions, scenarios, and uncertainty before making a recommendation.

Current status: experimental, `R3 / M3 / U0`. The repository has executable tooling and evaluated contracts, but there is no public practitioner validation or production-reliability claim. See [STATUS.md](STATUS.md) for the current maturity record.

## Why this project exists

Many AI systems produce fluent but hard-to-audit conclusions. This project makes strategic analysis more inspectable by turning a broad question into a decision memo with clear structure.

It helps teams:

- frame a decision rather than ask for a vague answer
- separate facts from inference
- compare alternatives explicitly
- identify what evidence would change the recommendation
- produce a reviewable artifact instead of a one-off narrative

This is not a legal or compliance engine. Human reviewers remain responsible for consequential decisions.

## What you get

- A portable reasoning contract: [SKILL.md](SKILL.md), with a [Russian mirror](SKILL_RU.md) and an additive [Codex overlay](codex/SKILL.md)
- Structured outputs: decision memos, scenario briefs, red-team briefs, and mixed-mode analysis
- A developer toolkit: the `gtta` CLI, a structured `MemoArtifact`, rendering utilities, contract checks, review bundles, and MCP tools
- Evidence handoff to [Agenda Intelligence MD](https://github.com/vassiliylakhonin/agenda-intelligence-md) for deterministic packet validation

The skill guides reasoning. The toolkit checks artifacts. Human reviewers own consequential decisions.

## Choose a starting point

| Your task | Start here |
| --- | --- |
| Give an agent the reasoning method | [Start with the skill](#start-with-the-skill) |
| Create or check a structured memo artifact | [Use the toolkit](#use-the-toolkit) |
| Inspect a complete worked case | [Examples](examples/README.md) |
| Understand the evidence behind the method | [Validation record](#examples-and-validation) and [STATUS.md](STATUS.md) |

## Start with the skill

Load [SKILL.md](SKILL.md) into your agent. Add the matching runtime overlay when applicable, then give the agent a concrete decision brief:

```text
Use Global Think Tank Analyst.
Question: What would justify a limited market-entry pilot?
Decision: enter, pilot, or wait.
Audience: operating committee.
Geography: specify the target jurisdiction.
Time horizon: next 12 months.
Evidence mode: reasoning-only; the case is hypothetical.
Separate assumptions from facts, compare alternatives, and state
what evidence would change the recommendation.
```

Choose the evidence mode explicitly:

- `live-source-backed`
- `user-provided sources`
- `illustrative source packet`
- `reasoning-only`

A reasoning-only memo must not imply that current sources were checked. For sourced work, supply the source packet or authorize collection, preserve provenance and dates, and disclose unresolved source conflicts. See the [analysis contract](docs/analysis-contract.md).

## Use the toolkit

From a checkout, with Python 3.10 or later:

```bash
python -m pip install -e '.[mcp,verification]'
gtta new --mode B --topic "Market-entry regulatory exposure"
gtta check-contract examples/sanctions-exposure-memo.md --mode B
gtta artifact-schema
gtta review examples/cookbooks/secondary-sanctions/memo.json --out-dir memo.review
```

`gtta new` prints a starting contract; an analyst or agent still has to complete the analysis. The secondary-sanctions example uses a synthetic packet.

Review bundles record checks and review metadata. Run `gtta mcp` to expose the toolkit to an MCP host. See the [contract checker](docs/contract-checker.md), [artifact schema and commands](docs/memo-artifact.md), and [review-bundle contract](docs/review-bundle.md).

## Repository layout

- `SKILL.md` — the reasoning method and task framing
- `SKILL_RU.md` — Russian-language mirror of the skill
- `codex/` — runtime overlay and Codex-specific guidance
- `docs/` — contracts, methodology, workflows, and integrations
- `examples/` — worked memos and scenario examples
- `evals/` — reviewer checklists, rubrics, and adversarial eval aids
- `signals/` — public signal snapshots and signal feed data
- `scripts/` — repo validation and tooling scripts
- `src/` — Python package code and CLI implementation

## How the repositories fit together

| Layer | Repository | Responsibility |
| --- | --- | --- |
| General reasoning | This repository | Decision framing, alternatives, uncertainty, and memo contracts |
| Regional reasoning | [Central Asia & Caspian](https://github.com/vassiliylakhonin/central-asia-caspian-hybrid-intelligence-skill) | Banking, ownership, sanctions, corridors, and energy in that region |
| Regional reasoning | [Gulf & Middle East](https://github.com/vassiliylakhonin/gulf-middle-east-hybrid-intelligence-skill) | Iran/GCC exposure, maritime chokepoints, and energy flows |
| Evidence checks | [Agenda Intelligence MD](https://github.com/vassiliylakhonin/agenda-intelligence-md) | Deterministic checks on supplied evidence packets |

Regional skills add local reasoning to the general method. The [evidence-packet handoff](docs/evidence-packet-handoff.md) is the primary verification seam. Loading the skills alone does not run or certify a real analysis.

## Examples and validation

When a memo relies on numerical scenarios, follow the [quantitative scenario handoff](docs/quantitative-scenario-handoff.md): preserve actual model runs and input provenance, explain constraints and ranking reversals, and distinguish scenario comparisons from optimization.

Start with the [example guide](examples/README.md), then compare:

| Example | What to inspect |
| --- | --- |
| [Sanctions exposure](examples/sanctions-exposure-memo.md) | Reasoning-only analysis and its limits |
| [Supplied supply-chain sources](examples/user-provided-sources-supply-chain-sanctions.md) | Provenance and bounded conclusions |
| [Conflicting demand forecasts](examples/source-conflict-iea-opec-demand-forecast.md) | Preserving disagreement in an illustrative packet |
| [Flagship portfolio cookbook](examples/cookbooks/flagship-portfolio/README.md) | Reproducible artifacts and evidence checks across two cases |

Historical source-backed examples are dated snapshots. Recheck current primary sources before reuse.

The evaluation record contains both positive development results and a null holdout result: the broader holdout showed no measured behavioral lift for either tested condition. Structural contract checks remained useful, but they are not a substitute for real-world validation.

## Documentation and contribution

- [Headless workflow](docs/headless-workflow.md) and [integrations](docs/integrations/) for automation interfaces and optional adapters
- [Research basis](docs/research-basis.md) and [maturity framework](docs/maturity-framework.md) for why the method exists and how claims are bounded
- [Public signal examples](signals/README.md): [latest](signals/latest.md), [archive index](signals/index.json), and [JSON Feed](signals/feed.json)
- [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md) for repository rules and constraints

Run the repository checks before submitting changes:

```bash
python3 scripts/check.py
```

This project supports analysis and review. It does not provide legal clearance, certify compliance, or execute enforcement decisions. Optional agent workflows are experimental and retain human review obligations.

## License

See [LICENSE](LICENSE).
