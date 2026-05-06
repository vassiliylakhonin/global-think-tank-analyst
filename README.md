# Global Think Tank Analyst

[![ClawHub](https://img.shields.io/badge/ClawHub-global--think--tank--analyst-2bc6a4)](https://clawhub.ai/vassiliylakhonin/global-think-tank-analyst)
[![CI](https://github.com/vassiliylakhonin/global-think-tank-analyst/actions/workflows/ci.yml/badge.svg)](https://github.com/vassiliylakhonin/global-think-tank-analyst/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**A universal AI-agent playbook for decision-ready geopolitical, policy, sanctions, trade, regulatory, and strategic-risk memos.**

Global Think Tank Analyst turns broad risk questions into structured, evidence-aware decision memos. It works as a skill, system prompt, repository context, RAG seed, or agent instruction pack for ChatGPT, Claude, Gemini, Perplexity, Cursor, Codex, OpenClaw, custom MCP agents, and internal analyst copilots.

The point is simple: help users move from "interesting geopolitical commentary" to "what decision should we make, what could change it, and how confident are we?"

## What users get

- A clear answer to the decision question, not a decorative background essay.
- Explicit separation between **facts**, **assumptions**, **assessments**, **scenarios**, and **unknowns**.
- Practical options with trade-offs, implementation friction, and triggers.
- Scenario thinking without false precision.
- Evidence-limit notices when an agent cannot verify live sources.
- A reusable memo structure that teams can apply across different AI tools.

## Use it with any AI agent

| Agent environment | Best way to use this repo |
|---|---|
| ChatGPT, Claude, Gemini, Perplexity | Paste the [universal agent prompt](AGENTS.md) or attach `SKILL.md` as context |
| Codex, Cursor, Windsurf, IDE agents | Add `AGENTS.md`, `llms.txt`, and `codex/SKILL.md` as repository context |
| OpenClaw / ClawHub | Install the packaged skill with `openclaw skills install vassiliylakhonin/global-think-tank-analyst` |
| Internal copilots / MCP agents | Index `llms.txt`, `SKILL.md`, `AGENTS.md`, and `signals/index.json` |
| RAG workflows | Use the signal archive as examples and `SKILL.md` as the behavior contract |

## Best for

- country risk briefs;
- sanctions and export-control exposure assessments;
- trade, tariff, and regulatory impact memos;
- geopolitical scenario briefs;
- stakeholder and incentives analysis;
- red-team challenges to an existing policy or risk view;
- leadership-facing strategic implications notes;
- founder, operator, investor, NGO, compliance, and public-policy decision support.

## Not for

- legal, compliance, investment, or intelligence advice;
- intelligence-style certainty;
- generic news summaries;
- academic literature reviews;
- unsupported numerical forecasting;
- prestige-sounding analysis with weak evidence.

## Output modes

| Mode | Use when you need | Typical output |
|---|---|---|
| **A - Quick Brief** | Fast orientation | Bottom line, why it matters, main risks, watchlist, confidence |
| **B - Standard Memo** | Default decision memo | Executive takeaway, context, evidence limits, actors, assessment, options |
| **C - Scenario Brief** | Divergent futures matter | Baseline, 2-4 scenarios, triggers, implications, indicators |
| **D - Red-Team Challenge** | Stress-test a claim | Failure modes, alternative explanations, missing assumptions, revised judgment |
| **E - Decision Briefing Pack** | A team needs to act | Memo, options table, watchlist, questions for owners, next-step cadence |

## Quick start

Paste this into any capable AI agent:

```text
Use Global Think Tank Analyst.

Question: [what we need answered]
Decision this informs: [what action, posture, prioritization, or escalation depends on it]
Audience: [founder / operator / investor / compliance team / policy team / leadership]
Geography: [countries, regions, corridors, markets]
Time horizon: [days / months / 1-3 years]
Evidence mode: source-backed / reasoning-only / mixed
Depth: quick brief / standard memo / scenario brief / red-team / decision briefing pack

Separate facts, assumptions, assessments, scenarios, and unknowns. Give options, trade-offs, indicators to watch, and bounded confidence.
```

If the agent has live browsing, ask it to cite sources. If it does not, it must say so and lower confidence.

## Strong default prompt

```text
Act as Global Think Tank Analyst.

Produce a decision-ready policy-risk memo, not a news summary. Start by framing the decision. Separate Fact, Assessment, Assumption, Scenario, and Unknown. If live verification was not performed, say exactly: EVIDENCE ACCESS LIMITED: no live verification performed in this environment.

End with:
1. Options and trade-offs
2. Indicators to watch
3. Confidence and key unknowns
4. What evidence would change the judgment
```

## What the memo always makes explicit

| Standard | How it appears |
|---|---|
| Decision framing | `Question`, `Decision`, `Audience`, `Time horizon`, `Evidence mode` |
| Evidence discipline | `Fact`, `Assessment`, `Assumption`, `Scenario`, `Unknown` labels |
| Evidence limits | Required notice when live/source verification was not performed |
| Uncertainty | `Low`, `Moderate`, or `High` confidence tied to evidence quality |
| Practical relevance | Options, trade-offs, implementation friction, and indicators to watch |
| Actionability | Triggers that change posture, not generic "monitor closely" advice |

## Policy Risk Signal - public examples

Short, source-aware policy risk notes showing how this agent playbook turns public signals into decision-ready analysis.

- [2026-04-28](signals/2026/2026-04-28.md): Evidence discipline is the product, not decoration

[Full signal archive](signals)

## Automated signal pipeline

The repository includes a weekly GitHub Actions pipeline that drafts the next Policy Risk Signal from public RSS/Atom sources and opens a pull request for review.

How it works:

1. Fetch public source snippets from `.github/policy-risk-signal/sources.json`.
2. Generate one short source-aware signal with `scripts/generate_policy_risk_signal.py`.
3. Write `signals/YYYY/YYYY-MM-DD.md` and update the README/archive indexes.
4. Open a pull request instead of publishing directly to `main`.

Required setup:

- add repository secret `OPENAI_API_KEY`;
- optionally set repository variable `OPENAI_MODEL`;
- run the **Policy Risk Signal** workflow manually once, then let the weekly schedule continue.

The review step is intentional: policy-risk content should be checked before publication.

## Agent-readable endpoints

- [`AGENTS.md`](AGENTS.md) - universal instruction contract for AI agents;
- [`llms.txt`](llms.txt) - quick orientation for LLMs and agent indexers;
- [`SKILL.md`](SKILL.md) - canonical skill behavior;
- [`codex/SKILL.md`](codex/SKILL.md) - Codex-ready variant;
- [`signals/latest.md`](signals/latest.md) - latest signal in markdown;
- [`signals/index.json`](signals/index.json) - machine-readable signal index;
- [`signals/feed.json`](signals/feed.json) - JSON Feed for automated ingestion.

## Relationship to Agenda-Intelligence.md

This repository is the full memo and decision-support layer.

For a lighter, portable markdown layer that any AI agent can use before summarizing public agenda, see [Agenda-Intelligence.md](https://github.com/vassiliylakhonin/Agenda-Intelligence-md).

Use them together like this:

```text
Agenda-Intelligence.md = small universal protocol for agenda triage
Global Think Tank Analyst = full memo skill for decision-ready policy risk analysis
```

Global Think Tank Analyst can use Agenda-Intelligence.md principles for agenda triage, signal classification, uncertainty labels, scenarios, and watch-next indicators.

## Installation and integration

### OpenClaw / ClawHub

```bash
openclaw skills install vassiliylakhonin/global-think-tank-analyst
```

Then ask for a policy-risk memo, scenario brief, red-team challenge, or decision briefing pack. The skill will activate when the request matches its domain.

### Codex

Use:

```text
codex/SKILL.md
AGENTS.md
llms.txt
```

### Any AI agent

Attach or paste:

```text
AGENTS.md
SKILL.md
```

For retrieval systems, index:

```text
llms.txt
SKILL.md
AGENTS.md
signals/index.json
signals/latest.md
```

## Example prompts

### Quick Brief

```text
Prepare a quick brief on EU CBAM exposure for a Kazakh metals exporter over the next 12 months.
```

### Standard Memo

```text
Write a policy-risk memo on sanctions exposure for a Russian energy company operating in Central Asia.
```

### Scenario Brief

```text
Provide a scenario brief on possible US-China semiconductor control developments for 2026-2028.
```

### Red-Team Challenge

```text
Red-team the claim that supply-chain sanctions risk for a European technology firm is manageable.
```

### Decision Briefing Pack

```text
Create a decision briefing pack for a logistics company deciding whether to reroute shipments away from a higher-risk customs corridor.
```

## Repository structure

```text
.
├── AGENTS.md             # Universal AI-agent instructions
├── SKILL.md              # Canonical skill behavior
├── codex/SKILL.md        # Codex-ready variant
├── llms.txt              # Agent and LLM indexer orientation
├── README.md             # Public documentation
├── signals/              # Policy Risk Signal archive
├── scripts/              # Signal generation automation
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
└── .github/              # CI, issue templates, PR template, workflows
```

## Trust and safety posture

This project is intentionally conservative about evidence. It should not fabricate sources, imply live verification when none occurred, or present speculative geopolitical judgments as facts.

It is a decision-support tool, not legal, compliance, investment, or intelligence advice.

## License

MIT - see [LICENSE](LICENSE).
