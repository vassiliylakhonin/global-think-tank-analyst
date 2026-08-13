# Examples

These examples show how Global Think Tank Analyst turns broad policy, sanctions, trade, regulatory, and geopolitical questions into decision-shaped memos.

Use them as a learning path, not as operational advice. Examples marked `live-source-backed` cite public sources retrieved on the date stated in the memo; verify current facts before using them for any real decision.

## Freshness policy

The `live-source-backed` label is a snapshot, not a recency guarantee. Each example carries a retrieval date in its body.

- **Re-verify** an example before treating any cited fact as current if its retrieval date is **older than 6 months**. The decision frame and reasoning structure remain useful; the specific facts may not.
- **Re-verify sooner — within 30 to 90 days —** when the example covers a fast-moving domain: sanctions designations, OFAC / EU lists, tariff rates, regulatory effective dates, central-bank rate decisions, active enforcement actions. Recency expectations in these domains are weeks, not months.
- **Archive or replace** an example when a cited fact has been materially superseded (new rule, lifted sanction, revised tariff) and the memo's judgment depends on the superseded fact. Move the file to `examples/archive/` with a header note pointing to the replacement, or update the example in place and bump its retrieval date.

Examples that fail this policy and are kept anyway should be relabeled from `live-source-backed` to `illustrative source packet` so the evidence mode matches reality.

## Learning path

1. Start with [`sanctions-exposure-memo.md`](sanctions-exposure-memo.md) to see the basic reasoning-only memo structure: decision frame, evidence limits, risks, options, indicators, confidence.
2. Read [`live-source-backed-memo.md`](live-source-backed-memo.md) to see the same structure with public sources and explicit facts / assessments / assumptions.
3. Read [`mixed-mode-middle-corridor-logistics-risk.md`](mixed-mode-middle-corridor-logistics-risk.md) to see how a `live-source-backed` memo stops at the boundary of the source actually retrieved instead of using inaccessible sources.
4. Compare the paired projection files in [`agenda-projections/`](agenda-projections/) to see how a memo can be mapped into Agenda Intelligence MD JSON for validation and evidence-aware scoring.
5. Read [`user-provided-sources-supply-chain-sanctions.md`](user-provided-sources-supply-chain-sanctions.md) to see the mode where the user's own documents become the primary evidence base.
6. Use [`red-team-policy-brief.md`](red-team-policy-brief.md) when you need to challenge an existing claim rather than draft a neutral memo.
7. Read [`source-conflict-iea-opec-demand-forecast.md`](source-conflict-iea-opec-demand-forecast.md) to see the **source-conflict-surfacing rule** applied: two reputable sources disagree on a load-bearing fact; the memo names both with provenance, assesses source independence, states a preferred position with reasoning, and carries the conflict through to the decision instead of silently averaging.

## Evidence modes

| Evidence mode | What it means | Start here |
|---|---|---|
| `reasoning-only` | No live sources checked; the memo must disclose evidence limits and lower confidence. | [`sanctions-exposure-memo.md`](sanctions-exposure-memo.md) |
| `live-source-backed` | Public sources were retrieved and cited for the example. | [`live-source-backed-memo.md`](live-source-backed-memo.md) |
| `live-source-backed` | One primary source was retrieved; unsupported legal and compliance claims are accounted for but excluded from the conclusion. | [`mixed-mode-middle-corridor-logistics-risk.md`](mixed-mode-middle-corridor-logistics-risk.md) |
| `user-provided sources` | The user's own documents, registers, classifications, or notes are treated as the evidence base. | [`user-provided-sources-supply-chain-sanctions.md`](user-provided-sources-supply-chain-sanctions.md) |

## Domain examples

| Domain | Example |
|---|---|
| Sanctions / AML | [`live-source-backed-memo.md`](live-source-backed-memo.md) |
| Energy / commodities | [`live-source-backed-hormuz-energy-prices.md`](live-source-backed-hormuz-energy-prices.md) |
| Regulatory / AI policy | [`live-source-backed-eu-ai-act-simplification.md`](live-source-backed-eu-ai-act-simplification.md) |
| Trade / critical minerals | [`live-source-backed-china-critical-minerals-suspension.md`](live-source-backed-china-critical-minerals-suspension.md) |
| Trade / customs / climate | [`live-source-backed-cbam-enforcement.md`](live-source-backed-cbam-enforcement.md) |
| Monetary policy / corporate finance | [`live-source-backed-ecb-rate-hold.md`](live-source-backed-ecb-rate-hold.md) |
| Geopolitical scenarios | [`geopolitical-scenario-brief.md`](geopolitical-scenario-brief.md) |
| AI governance | [`ai-governance-scenario-brief.md`](ai-governance-scenario-brief.md) |
| Central Asia / sanctions / logistics | [`mixed-mode-middle-corridor-logistics-risk.md`](mixed-mode-middle-corridor-logistics-risk.md) |
| Energy / source-conflict method demonstration | [`source-conflict-iea-opec-demand-forecast.md`](source-conflict-iea-opec-demand-forecast.md) |

## How to judge an example

A strong example should:
- state the decision it informs;
- declare evidence mode and confidence;
- separate facts, assessments, assumptions, scenarios, and unknowns;
- identify actor incentives and leverage where relevant;
- present options with trade-offs;
- give concrete watch-next indicators;
- say what evidence would change the judgment.

Use [`../evals/checklist.md`](../evals/checklist.md) for a fuller human review pass.
