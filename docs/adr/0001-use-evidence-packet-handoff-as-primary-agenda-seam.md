# Use the evidence-packet handoff as the primary Agenda seam

Status: accepted — 2026-07-15

## Context

Global Think Tank Analyst produces a memo with facts, assessments, assumptions, scenarios, and unknowns. Agenda Intelligence MD v1.3.0 now leads with a smaller `claims[] + sources[]` evidence-packet contract. The older agenda-brief, scoring, `analyze`, and MCP contracts still exist, but treating them as the primary seam makes the two repositories look more tightly coupled than they are.

## Decision

The primary composition seam is an evidence-packet handoff containing externally checkable factual and quantitative claims plus caller-supplied source text. Assessments, scenarios, assumptions, and analyst judgments remain in the memo. The older strategic-intelligence contracts are compatibility paths.

## Consequences

- The reasoning skill remains runtime-neutral.
- Agenda Intelligence can lint packet completeness without pretending to validate the memo's judgment.
- Existing `analyze`, memo-schema, scoring, and MCP examples remain historical compatibility evidence.
- The handoff shape is documented and guarded in CI without vendoring Agenda Intelligence's schema.
