# Global Think Tank Analyst

[![CI](https://github.com/vassiliylakhonin/global-think-tank-analyst/actions/workflows/ci.yml/badge.svg)](https://github.com/vassiliylakhonin/global-think-tank-analyst/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Strategic-risk analysis skill for AI agents.**

A reusable domain skill for agents that produce policy-risk, sanctions, regulatory, geopolitical, trade, and strategic-risk memos.

LLMs are good at summarizing geopolitical events. They are weak at turning them into decision-ready intelligence: framing the decision, separating facts from assessments, stating uncertainty, reasoning through actor incentives, identifying scenarios, and defining what to watch next.

This repository is a domain skill layer that teaches agents how to do that work. It is a behavior contract, not a framework, runtime, or eval platform.

## What it does

- frames broad geopolitical or policy questions as decision problems;
- separates facts, assessments, assumptions, scenarios, and unknowns;
- produces structured strategic-risk memos in five modes (quick brief, standard, scenario, red-team, decision pack);
- enforces evidence-boundary language when live verification is not possible;
- avoids unsupported certainty and source theater;
- helps agents produce concrete watch-next indicators and decision triggers;
- gives a reusable analyst behavior contract that travels across runtimes.

## What it is not

- not an autonomous intelligence system;
- not a factuality verifier;
- not a live source retriever or RAG pipeline;
- not legal, compliance, sanctions, or investment advice;
- not a generic agent framework, CLI tool, or MCP server;
- not a benchmarked evaluation framework;
- not a replacement for human analyst judgment.

If you need validation, scoring, evidence audit, schemas, CLI, MCP, or CI checks for outputs produced with this skill, see the companion project [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md).

## Portfolio: how this skill composes

Three layers, separately maintained, designed to compose:

| Layer | Repo | What it does |
|---|---|---|
| **Horizontal domain skill** | **Global Think Tank Analyst** (this repo) | The reasoning method and memo modes. Region- and topic-agnostic. |
| **Vertical specialists** | [central-asia-caspian-hybrid-intelligence-skill](https://github.com/vassiliylakhonin/central-asia-caspian-hybrid-intelligence-skill) | Region-deep skills that ride on top of the horizontal method (Central Asia & Caspian: sanctions, AML, corridors, banking, logistics, energy, geopolitical risk). |
| **Infrastructure / validation** | [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md) | Machine-readable protocol, schemas, validation, scoring, evidence audit, CLI / MCP / CI tooling. |

```mermaid
flowchart LR
    A[Global Think Tank Analyst<br/>horizontal method] -->|drafts memo| D[Strategic-risk memo]
    V[Vertical specialist<br/>e.g. Central Asia Caspian] -->|adds regional depth| D
    D -->|validated, scored| C[Agenda Intelligence MD<br/>infrastructure]
    C --> O[Decision-ready brief]
```

> Use **Global Think Tank Analyst** for the analyst behavior and memo structure. Bring in a **vertical specialist** when the domain or region needs depth this skill alone cannot provide. Use **Agenda Intelligence MD** to validate, score, and audit the output.

This repo does not duplicate either neighbor. Vertical depth lives in vertical-specialist repos; validation and tooling live in Agenda Intelligence MD.

For a concrete CLI / MCP recipe (score a memo, validate a JSON projection, add an evidence pack), see [`docs/integrations/agenda-intelligence-md.md`](docs/integrations/agenda-intelligence-md.md).

## Integration status

| Environment | Status | Notes |
|---|---|---|
| Codex / Cursor / Windsurf | Compatible by repo context | Add `AGENTS.md`, `SKILL.md`, `codex/SKILL.md`, `llms.txt` as context |
| ChatGPT, Claude, Gemini, Perplexity | Compatible by paste/attach | Paste `AGENTS.md` or attach `SKILL.md` |
| OpenClaw / ClawHub | Packaging-dependent | Install only if a current package exists for your version |
| RAG / internal copilots | Compatible by indexing | Index `README.md`, `SKILL.md`, `AGENTS.md`, `llms.txt`, `signals/` |
| Agenda Intelligence MD | Companion project | Use it for validation, evidence audit, scoring |
| MCP server | Not implemented here | Use Agenda Intelligence MD if MCP is required |
| CLI validation | Not implemented here | Use Agenda Intelligence MD |
| Factuality verification | Not implemented here | This skill enforces *discipline*, not truth |

This repository ships only markdown skill files, examples, eval checklists, and a small signal-generation script. It does not include validators, schemas, or runtimes.

## Quick usage

Paste this into any capable AI agent:

```text
Use Global Think Tank Analyst.

Question: [what we need answered]
Decision this informs: [what action depends on it]
Audience: [founder / operator / investor / compliance / policy team / leadership]
Geography: [countries, regions, corridors, markets]
Time horizon: [days / months / 1–3 years]
Evidence mode: source-backed / reasoning-only / mixed
Depth: quick brief / standard memo / scenario brief / red-team / decision pack

Separate facts, assumptions, assessments, scenarios, and unknowns.
Give options, trade-offs, indicators to watch, and bounded confidence.
```

If the agent has live browsing, ask it to cite sources. If it does not, it must say so and lower confidence.

## Memo modes

| Mode | Use when you need | Typical output |
|---|---|---|
| **A — Quick Brief** | Fast orientation | Bottom line, why it matters, main risks, watchlist, confidence |
| **B — Standard Memo** | Default decision memo | Executive takeaway, context, evidence limits, actors, assessment, options |
| **C — Scenario Brief** | Divergent futures matter | Baseline, 2–4 scenarios, triggers, implications, indicators |
| **D — Red-Team Challenge** | Stress-test a claim | Failure modes, alternative explanations, missing assumptions, revised judgment |
| **E — Decision Briefing Pack** | A team needs to act | Memo, options table, watchlist, questions for owners, next-step cadence |

## Before / after

A generic LLM answer to *"What is the sanctions risk for a European tech firm with operations in Central Asia?"*:

> The geopolitical landscape in Central Asia is complex. Companies should be aware of secondary sanctions risk and monitor developments closely. Engaging stakeholders and remaining agile will be important. Overall the situation requires careful attention.

A Global Think Tank Analyst-style answer to the same question:

> **Question:** Sanctions exposure for a European tech firm operating in Central Asia.
> **Decision:** Whether to expand, hold, or contract Central Asia operations over 12 months.
> **Evidence mode:** reasoning-only.
> EVIDENCE ACCESS LIMITED: no live verification performed in this environment.
>
> **Key judgment (Moderate confidence):** Secondary-sanctions risk is concentrated in dual-use tech and financial-rail exposure, not in general commercial activity. The dominant uncertainty is enforcement posture, not legal text.
>
> **Fact:** EU and US export-control regimes apply extraterritorially to certain dual-use items.
> **Assessment:** Local banking partners, not the firm, are the primary transmission channel for secondary risk.
> **Assumption:** Current sanctions architecture remains broadly stable for 12 months.
> **Scenarios:** (1) Stable enforcement, narrow exposure. (2) Targeted enforcement against re-export corridors raises compliance cost. (3) Broad financial-rail action forces partner switching.
> **Actor incentives:** Local banks want correspondent access; regulators want optionality; the firm wants predictability.
> **Options:** (a) Maintain with stronger partner due diligence; (b) Ring-fence dual-use SKUs; (c) Restructure payment rails through a compliant hub.
> **Watch next:** New OFAC/EU designations naming regional banks; tightening of re-export thresholds; partner KYC escalation.
> **What would change the judgment:** Direct enforcement against a comparable peer; new dual-use list additions covering core SKUs.

The first answer is a tone. The second is a decision input.

## Examples

Worked memos in [`examples/`](examples/):

- [Sanctions exposure memo](examples/sanctions-exposure-memo.md)
- [Regulatory impact memo](examples/regulatory-impact-memo.md)
- [Geopolitical scenario brief](examples/geopolitical-scenario-brief.md)
- [Red-team policy brief](examples/red-team-policy-brief.md)

All examples use **reasoning-only / illustrative** evidence mode. They do not cite live sources and are not intelligence products.

## Evaluation

Lightweight, honest review materials in [`evals/`](evals/):

- [`checklist.md`](evals/checklist.md) — human review checklist
- [`failure-modes.md`](evals/failure-modes.md) — common failure patterns
- [`rubric.md`](evals/rubric.md) — starter scoring rubric

These are *human review aids*, not a validated benchmark. For machine-readable validation, scoring, and audit, use [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md).

## Signal archive

[`signals/`](signals/) holds short public examples of the skill style: one signal, why it matters, a bounded assessment, and indicators to watch.

The archive is:

- a public set of *examples* of how the skill produces output;
- not official intelligence;
- not investment, legal, or compliance advice;
- not a guarantee of factual verification beyond what each signal explicitly cites.

To contribute a signal, copy [`signals/TEMPLATE.md`](signals/TEMPLATE.md).

## Agent-readable endpoints

- [`AGENTS.md`](AGENTS.md) — universal instruction contract for AI agents
- [`SKILL.md`](SKILL.md) — canonical skill behavior
- [`codex/SKILL.md`](codex/SKILL.md) — Codex-ready variant
- [`llms.txt`](llms.txt) — orientation for LLMs and agent indexers
- [`signals/index.json`](signals/index.json) — machine-readable signal index
- [`signals/feed.json`](signals/feed.json) — JSON Feed for ingestion

## Naming

- **Product:** Global Think Tank Analyst
- **Method:** Policy Risk Memo Architect (the analyst behavior the product implements)
- **Companion infrastructure:** Agenda Intelligence MD

## Repository structure

```text
.
├── AGENTS.md             # Universal AI-agent instructions
├── SKILL.md              # Canonical skill behavior
├── codex/SKILL.md        # Codex-ready variant
├── llms.txt              # Agent and LLM indexer orientation
├── examples/             # Worked memo examples
├── evals/                # Human review checklist, failure modes, rubric
├── signals/              # Public signal archive + template
├── scripts/              # Signal generation helper
└── .github/              # CI, issue templates, workflows
```

## Limitations

- This project is intentionally conservative about evidence. It does not fabricate sources, imply live verification when none occurred, or present speculative geopolitical judgments as facts.
- It is a **decision-support skill**, not legal, compliance, investment, sanctions, or intelligence advice.
- It does not verify factuality. It enforces analytical *discipline* — fact/assessment/assumption/scenario/unknown separation, evidence-limit disclosure, scenario framing.
- It does not retrieve sources, run validators, expose an MCP server, or score outputs. For those, use [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md).
- Examples in this repo are illustrative (`reasoning-only / illustrative source packet`). Do not treat them as real intelligence products.
- Signals in `signals/` are public examples of the skill style, not official intelligence and not real-time.

## Roadmap

Directional, not committed. Items here are not implemented.

- More worked examples across additional domains (export controls, critical minerals, energy transition policy).
- Tighter integration recipes for Agenda Intelligence MD (validation/scoring of memos produced with this skill).
- Additional failure-mode patterns derived from real review feedback.
- Expanded signal archive with a wider domain coverage and clearer evidence-mode tagging.

If you'd like to influence the roadmap, open an issue.

## License

MIT — see [LICENSE](LICENSE).
