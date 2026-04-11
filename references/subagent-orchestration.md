# Subagent Orchestration Runbook

Use this flow for high-stakes or deep analysis.

## Roles

1. **collector**: gather factual baseline and source list
2. **analyst**: build main thesis, drivers, and scenarios
3. **red-team**: challenge assumptions and produce competing hypotheses
4. **editor**: merge outputs into one decision memo

## Handoff contract

Each role returns:
- `claims`: key claims (bullets)
- `evidence`: source-backed points with date
- `unknowns`: missing data
- `confidence`: high/medium/low/speculative with 1-line rationale

## Merge rules

- Keep only claims that survived red-team challenge.
- Flag unresolved disagreements explicitly.
- End with Go/No-Go thresholds + 1-2 week validation plan.
