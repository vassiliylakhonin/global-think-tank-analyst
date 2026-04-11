# Eval Pack (Regression Gate)

Use this for release or major prompt updates.

## Test set

Maintain 20-30 fixed prompts across:
- country risk
- sanctions/trade policy
- security trend assessment
- scenario planning
- red-team challenge

## Quality gates

For each output, score 0-2 on:
- correctness
- relevance
- actionability
- risk transparency

## Release decision

- **Go**: average >= 1.6 and no critical failures
- **Conditional Go**: 1.3-1.59 or <=2 critical issues
- **No-Go**: < 1.3 or repeated critical failures

## Critical failure examples

- fabricated evidence presented as fact
- no assumptions in deep analysis
- missing alternative hypothesis under high uncertainty
- no trigger-based decision criteria
