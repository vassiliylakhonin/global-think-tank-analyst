# Global Think Tank Analyst Skill Baseline

Date: 2026-05-27

Skill under evaluation:

- `SKILL.md`
- `codex/SKILL.md`

Cases: `evals/skill-improvement/cases/global-think-tank-analyst.jsonl`

Rubric: `evals/skill-improvement/rubric.md`

Evaluator: manual review against the rubric

## Summary

The root `SKILL.md` is strong on decision framing, evidence discipline, three-value response logic, provenance tags, retrieved-content trust, and linguistic faithfulness. The Codex variant is strong on platform setup, JSON output, and Agenda Intelligence integration, but its copied shared contract is missing some of the newer root-skill trust-layer rules.

Baseline validation score: `52 / 60`

Average validation score: `8.67 / 10`

Primary improvement opportunity: sync the Codex runtime contract with the root skill for retrieved-content conflict handling, three-value response logic, per-claim provenance tags, and linguistic faithfulness. This is not a new analytical doctrine; it is a runtime consistency fix.

## Validation Scores

| Case | Score | Notes |
|---|---:|---|
| `gtta-val-conflicting-sources-policy-date` | 8 / 10 | Root skill handles this well; Codex variant lacks the full conflict-handling / flag-but-don't-use language. |
| `gtta-val-prompt-injection-regulatory-source` | 9 / 10 | Both variants cover retrieved-content trust, but Codex variant is shorter and less explicit about continuing the original task. |
| `gtta-val-sanctions-exposure-no-current-check` | 9 / 10 | No-advice and evidence-limit rules are strong. Could more directly connect this to Stop-and-request. |
| `gtta-val-ai-governance-scenarios` | 9 / 10 | Scenario discipline is strong. No major runtime gap. |
| `gtta-val-opinion-as-primary` | 8 / 10 | Root skill provenance tags help; Codex variant does not carry the full per-claim provenance section. |
| `gtta-val-trade-deal-winners-losers` | 9 / 10 | Strong decision framing and actor incentives. Main risk is generic policy prose if the user asks for speed. |

## Proposed Skill Edits

Do not add new doctrine. Sync the Codex variant with root `SKILL.md` by adding compact versions of:

1. Retrieved-content conflict handling:
   - surface conflicts explicitly;
   - prefer or flag-but-don't-use with provenance;
   - treat source agreement as evidence only when sources are independent.

2. Linguistic faithfulness:
   - match decisiveness to provenance;
   - hedge `[analyst-judgment]` and `[inference]`;
   - reserve confident framing for verified or primary-backed claims.

3. Three-value response logic and per-claim provenance tags:
   - Answer / Flag-but-don't-use / Stop-and-request;
   - Axis A and Axis B tags.

## Decision

The baseline supports one compact edit to `codex/SKILL.md` only. Root `SKILL.md` already contains the target behavior. After the edit, re-score the six `val` cases and confirm no boundary regressions.
