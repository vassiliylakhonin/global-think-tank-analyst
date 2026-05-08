# AGENTS.md

## Project identity

Global Think Tank Analyst is a strategic-risk analysis skill for AI agents.

It is a domain reasoning layer, not an agent framework, CLI tool, factuality verifier, MCP server, or eval infrastructure project.

Use this positioning:

> Strategic-risk analysis skill for AI agents.

Longer description:

> A reusable domain skill for agents that produce policy-risk, sanctions, regulatory, geopolitical, trade, and strategic-risk memos with explicit evidence boundaries, uncertainty, scenarios, actor incentives, trade-offs, and watch-next indicators.

## Relationship to Agenda Intelligence MD

Global Think Tank Analyst:
- teaches the agent how to reason
- defines memo modes and analytical workflow
- handles domain framing
- produces strategic-risk memos

Agenda Intelligence MD:
- validates output structure
- provides schemas
- supports evidence/eval/CLI/MCP/CI tooling
- audits or scores outputs where implemented

Do not duplicate Agenda Intelligence MD inside this repo. When referencing validation, scoring, CLI, MCP, schemas, or CI checks, point to Agenda Intelligence MD unless this repo actually implements them.

## Honesty rules

Do not invent:
- metrics
- benchmarks
- adoption numbers
- source verification
- legal/compliance/investment advice
- production usage
- direct integrations that do not exist

Do not use exaggerated claims:
- revolutionary
- production-grade
- guarantees correctness
- solves hallucinations
- fully autonomous intelligence

If a feature is illustrative, planned, or experimental, label it clearly.

## Evidence rules

Every example must state its evidence mode:
- live-source-backed
- user-provided sources
- illustrative source packet
- reasoning-only

Do not fabricate citations, dates, sanctions details, legal conclusions, market facts, or policy changes.

If sources are not actually retrieved or verified, say so.

## Recommended README structure

1. One-line positioning
2. Problem
3. What it does
4. What it is not
5. Relationship to Agenda Intelligence MD
6. Quick usage
7. Memo modes
8. Before / after
9. Examples
10. Eval checklist / failure modes
11. Signal archive
12. Limitations
13. Roadmap

## Examples

Examples should show:
- user question
- evidence mode
- decision context
- key judgment
- facts vs assessments
- assumptions
- uncertainty
- actor incentives / leverage
- scenarios
- options / trade-offs
- watch-next indicators
- confidence
- what would change the judgment

## Eval docs

Eval docs should be lightweight and honest.

Use terms like:
- review checklist
- starter rubric
- failure modes

Do not call it a validated benchmark unless benchmark cases and results actually exist.

## Naming

Use consistent hierarchy:

Product: Global Think Tank Analyst

Method: Policy Risk Memo Architect

Companion infrastructure: Agenda Intelligence MD

Do not present these as competing names.

## Definition of done

A senior AI or agent engineering reviewer should understand that this repo is not a generic prompt pack. It should read as an early but credible domain skill layer for high-stakes strategic-risk agents.

---

## Runtime agent behavior

Operational behavior for agents *executing* the skill (memo intake, evidence labels, output modes, self-check) lives in [`SKILL.md`](SKILL.md). Treat this AGENTS.md as project-level rules; treat SKILL.md as runtime instructions.
