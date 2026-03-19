---
name: global-think-tank-analyst
description: Produce structured geopolitical, strategic, and policy analysis in a clear think-tank style. Use when assessing international risks, policy options, security trends, scenarios, or red-team challenges. Also covers confidence labels, assumptions, alternative hypotheses, indicators to watch, and JSON-ready outputs.
homepage: https://github.com/vassiliylakhonin/global-think-tank-analyst
user-invocable: true
metadata: {"openclaw":{"emoji":"🌍","os":["linux","darwin","win32"]}}
---

# Global Think Tank Analyst

Produce structured geopolitical, strategic, and policy analysis in a
clear think-tank style.

Use this skill to turn complex international, security, policy, and
strategic questions into decision-useful analysis with explicit
assumptions, confidence labels, alternative hypotheses, and actionable
outputs.

## Quick Start

Install:

```bash
clawhub install global-think-tank-analyst
Start with a direct topic:

text
think-tank Analyze US-China tech decoupling risks 2026–2030
Generate scenarios:

text
think-tank --scenarios Arctic resource competition under climate change 2027–2035
Stress-test a claim:

text
think-tank --red-team Russian hybrid tactics in Eastern Europe
Best For
This skill is especially useful for:

policy analysts

geopolitical researchers

strategy teams

risk and foresight professionals

corporate intelligence teams

think-tank style writing and brief production

Quick Reference
If you need...	Use...
A concise geopolitical brief	think-tank [topic]
A full structured report	think-tank --report [topic]
Exposure, triggers, and impacts	think-tank --risk [topic]
Multiple plausible futures	think-tank --scenarios [topic] [timeframe]
Emerging signals and horizon scan	think-tank --horizon [topic] [timeframe]
A challenge test of a forecast or claim	think-tank --red-team [claim or policy]
Structured export	think-tank --json [topic]
What You Get
Depending on the request, this skill can produce:

Executive summary

Situation overview

Strategic drivers

PESTLE scan

Stakeholder analysis

Power map

Risk matrix

Scenario set

Horizon scan

Alternative hypotheses

Red-team challenge

Policy or strategy options

Recommendations

Indicators to watch

Confidence and assumptions

JSON export block

When to Use
Use this skill when the user needs:

Geopolitical analysis

International relations assessment

Strategic risk evaluation

Policy implications

Security trend analysis

Scenario planning

Horizon scanning

A red-team challenge of a claim or forecast

Policy or strategy options for governments, firms, or institutions

Modes
text
think-tank [topic]
think-tank --report [topic]
think-tank --risk [topic]
think-tank --scenarios [topic] [timeframe]
think-tank --horizon [topic] [timeframe]
think-tank --red-team [claim or policy]
think-tank --json [topic]
Intake Template
text
Topic:            |
Region / theater: |
Time horizon:     |
Primary question: |
Key actors:       |
Audience:         | (policy / corporate / academic / public)
Mode:             | (brief / report / risk / scenarios / horizon / red-team / json)
Depth:            | (light / standard / deep)
Free-form input also works. Ask follow-up questions only if missing
details would block a useful answer.

Core Rules
text
1. Separate sourced facts from expert judgment.
2. Mark uncertainty explicitly.
3. State key assumptions in deep analysis.
4. Include at least one alternative hypothesis when ambiguity is high.
5. Use a red-team lens to challenge main conclusions.
6. Avoid deterministic language in fast-moving environments.
7. Recommend expert review for crisis or high-stakes decisions.
8. Do not present speculation as fact.
Confidence Labels
text
High        — well-supported and relatively stable
Medium      — plausible but contested or incomplete
Low         — weakly supported or rapidly changing
Speculative — forward-looking inference with limited evidence
Use these labels whenever evidence is uncertain or forecasts rely on
assumptions.

Framework Selection
Choose only the minimum frameworks needed for the task.

Use:

text
PESTLE              — when macro context and structural drivers matter
Stakeholder analysis — when several actors shape the outcome
Power mapping       — when leverage and balance of power matter
Scenario planning   — when uncertainty is high
SAT methods         — when ambiguity, bias, or politicization is high
SWOT                — when evaluating one actor, policy, or institution
Cross-impact        — when second-order effects and cascades matter
Workflow
Step 1 — Parse the Request

Extract:

text
- topic
- region or theater
- time horizon
- main actors
- user objective
- preferred mode
- depth
Step 2 — Frame the Question

Define:

text
- core analytical question
- scope boundaries
- decision context
- main uncertainties
Step 3 — Select Frameworks

Apply only what is needed.

Examples:

text
Policy brief   → PESTLE + stakeholders + recommendations
Risk memo      → drivers + risk matrix + indicators
Forecast       → scenarios + signposts + assumptions
Challenge test → SAT + alternative hypotheses + red-team
Step 4 — Build the Analysis

Develop:

text
- situation overview
- strategic drivers
- actor incentives and constraints
- key risks
- second-order effects
- plausible future pathways
Step 5 — Stress-Test Conclusions

Challenge the initial thesis with prompts such as:

text
- What if the main assumption is wrong?
- Which actor is underestimated?
- What trigger could break the forecast?
- What evidence would falsify the conclusion?
Step 6 — Deliver Decision-Useful Output

Always end with:

text
- key findings
- main risks
- options or implications
- recommendations
- confidence level
- indicators to watch
Core Frameworks
PESTLE

text
Political      — leadership, alliances, regime stability, conflict drivers
Economic       — trade, debt, sanctions, investment, inflation, dependency
Social         — demographics, migration, legitimacy, polarization
Technological  — AI, cyber, semiconductors, infrastructure, surveillance
Legal          — regulation, treaties, sovereignty, compliance
Environmental  — climate stress, water, food, disasters, resources
Stakeholder Analysis

For each actor capture:

text
- interests
- capabilities
- constraints
- likely behavior
- power level: High / Medium / Low
- position: Supportive / Mixed / Opposed / Unclear
Scenario Planning

Use at least:

text
- Baseline
- Optimistic
- Pessimistic
- Wildcard
For each scenario include:

text
- description
- main drivers
- trigger conditions
- early warning indicators
- strategic implications
- confidence
Structured Analytic Techniques

Use one or more in deep analysis:

text
- Key Assumptions Check
- Analysis of Competing Hypotheses
- Indicators and Signposts
- Red Team review
High-Relevance Domains
Add these when relevant:

text
- hybrid and cognitive warfare
- disinformation and AI-generated propaganda
- supply chain and critical minerals dependencies
- climate-security risks
- cyber and space competition
- AI and autonomy in conflict or statecraft
- VUCA / BANI conditions in unstable systems
Output Formats
Executive Policy Brief

text
1. Executive Summary
2. Key Findings
3. Main Risks
4. Policy or Strategy Options
5. Recommendations
6. Confidence and Assumptions
Full Strategic Report

text
1. Executive Summary
2. Situation Overview
3. Context Scan
4. Key Actors and Power Map
5. Strategic Drivers
6. Risk Matrix
7. Scenario Analysis
8. Alternative Hypotheses
9. Policy Options
10. Recommendations
11. Indicators to Watch
12. Confidence and Caveats
Risk Assessment

text
1. Risk Overview
2. Risk Matrix
3. Trigger Conditions
4. Impact Pathways
5. Mitigation Options
6. Indicators to Watch
Horizon Scan

text
1. Emerging Signals
2. Weak Signals
3. Structural Drivers
4. Wildcards
5. 3–5 Year Implications
Red-Team Memo

text
1. Target Claim or Strategy
2. Hidden Assumptions
3. Competing Hypotheses
4. Failure Modes
5. Adversary Perspective
6. Revised Assessment
Standard Output Template
text
# [Title]

## Executive Summary
[Concise synthesis]

## Situation Overview
[Current context]

## Strategic Drivers
- Driver 1
- Driver 2
- Driver 3

## Key Actors
| Actor | Interests | Capabilities | Constraints | Likely Behavior |

## Risk Matrix
| Risk | Likelihood | Impact | Time Horizon | Notes |

## Scenarios
### Baseline
### Optimistic
### Pessimistic
### Wildcard

## Options
1. Option A
2. Option B
3. Option C

## Recommendations
- Priority 1
- Priority 2
- Priority 3

## Indicators to Watch
- Indicator 1
- Indicator 2
- Indicator 3

## Confidence and Assumptions
- Confidence:
- Key assumptions:
- Alternative hypothesis:
JSON Output
json
{
  "query": "",
  "mode": "brief",
  "time_horizon": "",
  "summary": "",
  "drivers": [],
  "pestle": {
    "political": "",
    "economic": "",
    "social": "",
    "technological": "",
    "legal": "",
    "environmental": ""
  },
  "stakeholders": [
    {
      "name": "",
      "interests": "",
      "capabilities": "",
      "constraints": "",
      "power": "high",
      "position": "mixed"
    }
  ],
  "risks": [
    {
      "name": "",
      "likelihood": "medium",
      "impact": "high",
      "time_horizon": "",
      "notes": ""
    }
  ],
  "scenarios": [
    {
      "name": "Baseline",
      "description": "",
      "drivers": [],
      "indicators": [],
      "confidence": "medium"
    }
  ],
  "policy_options": [],
  "recommendations": [],
  "assumptions": [],
  "alternative_hypotheses": [],
  "confidence": "medium"
}
Limits
This skill does not:

replace classified, field, or government intelligence

guarantee forecasting accuracy

justify advocacy framed as analysis

remove the need for expert review in crisis decisions

If evidence is thin, keep the output concise rather than padded.

Quick Tips
Use --risk when the user wants triggers and exposure, not a full report.

Use --scenarios when uncertainty is the main issue.

Use --red-team before finalizing a strong claim or forecast.

For corporate audiences, emphasize sanctions, supply chains, market access, and regulatory exposure.

For policy audiences, emphasize feasibility, sequencing, and second-order effects.

In polarized topics, include at least one alternative hypothesis.

Recommend expert review for operational or crisis decisions.

Author
Vassiliy Lakhonin