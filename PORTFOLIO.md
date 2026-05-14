# Strategic-Risk Agent Portfolio

This portfolio is a small set of separately maintained repositories for
strategic-risk AI agents. The goal is not to create a monolith. The goal is to
keep reasoning method, regional depth, and validation infrastructure separate
enough that each part remains understandable and replaceable.

## What This Is

The portfolio has four assets:

| Layer | Repository | Role |
|---|---|---|
| Horizontal skill | [Global Think Tank Analyst](https://github.com/vassiliylakhonin/global-think-tank-analyst) | General strategic-risk memo method: policy, sanctions, regulatory, trade, geopolitical and scenario analysis. |
| Vertical specialist | [Central Asia + Caspian Hybrid Intelligence Skill](https://github.com/vassiliylakhonin/central-asia-caspian-hybrid-intelligence-skill) | Regional depth for Central Asia, Caspian corridors, sanctions / AML, banking, logistics, energy and geopolitical risk. |
| Vertical specialist | [Gulf + Middle East Hybrid Intelligence Skill](https://github.com/vassiliylakhonin/gulf-middle-east-hybrid-intelligence-skill) | Regional depth for Gulf, Iran, Iraq, maritime chokepoints, Iran sanctions, GCC banking, energy and sovereign wealth. |
| Infrastructure | [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md) | Schemas, validation, scoring, evidence audit, CLI / MCP tooling and package distribution. |

## What This Is Not

- Not a production intelligence platform.
- Not a factuality verifier.
- Not legal, compliance, sanctions, AML, investment, tax or trading advice.
- Not a claim of production usage or external validation.
- Not a guarantee that generated analysis is correct.

Each repository documents its own limitations. Operational use requires current
source verification and qualified professional review.

## How The Pieces Compose

Use the portfolio as a layered workflow:

1. Start with **Global Think Tank Analyst** when the task is broad: policy-risk
   framing, scenario analysis, red-team challenge, options and trade-offs.
2. Add a **vertical specialist** when the geography or transmission mechanism
   requires regional depth.
3. Use **Agenda Intelligence MD** when the output needs structure validation,
   evidence audit, scoring, CLI checks or MCP integration.

Example:

```text
Question: A European fintech is expanding onboarding in Kazakhstan and UAE-linked
trade corridors. What sanctions, AML, payment-rail and routing risks matter over
the next 6-12 months?

Use:
- Global Think Tank Analyst for memo structure and decision framing.
- Central Asia + Caspian skill for Kazakhstan / Caspian corridor mechanics.
- Gulf + Middle East skill for UAE / Iran-adjacent banking and trade exposure.
- Agenda Intelligence MD to validate or score a structured output.
```

## Choosing The Right Repository

Use **Global Think Tank Analyst** when:
- the question is cross-regional, policy-oriented or scenario-driven;
- you need memo structure more than regional domain depth;
- the output should separate facts, assumptions, assessments, scenarios and unknowns.

Use **Central Asia + Caspian Hybrid Intelligence Skill** when:
- the question involves Kazakhstan, Uzbekistan, Kyrgyzstan, Tajikistan,
  Turkmenistan, the Caspian, Middle Corridor, BO opacity, trade routing,
  sanctions adjacency, banking or energy corridors.

Use **Gulf + Middle East Hybrid Intelligence Skill** when:
- the question involves Iran sanctions, GCC banking, sovereign wealth,
  Gulf energy flows, Hormuz, Bab-el-Mandeb, Red Sea disruption, Iraq banking,
  or Iran-state / IRGC-affiliated / Iran-private distinctions.

Use **Agenda Intelligence MD** when:
- you need schemas, CLI, MCP, package installation, validation, scoring,
  evidence audit or machine-readable outputs.

## Design Principles

- **Separation of concerns:** reasoning method, regional depth and validation
  infrastructure stay in separate repositories.
- **Evidence discipline:** outputs should state evidence mode, confidence,
  uncertainty and source limits.
- **Honest status:** no repo should claim external validation, adoption,
  production use or benchmark status without evidence.
- **Composable assets:** each repo should be useful alone, but clearer when used
  with the others.
- **Small safe changes:** prefer validators, examples and clear docs over broad
  rewrites.

## Current Maturity

The portfolio is best understood as a set of early but credible public artifacts
for strategic-risk agent work. The repositories contain examples, skill
contracts, validators, signal archives and package tooling where implemented.

What remains open:

- external practitioner review;
- validated real-world case records;
- stronger source-anchored example coverage in every vertical;
- clearer public usage records if real use happens with permission;
- continued maintenance of agent-readable docs and signal metadata.

Do not treat the portfolio as externally validated until those gaps are closed.

