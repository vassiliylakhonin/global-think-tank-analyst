---
name: global-think-tank-analyst
description: Produce structured geopolitical, strategic, and policy analysis in a clear think-tank style, with assumptions, confidence labels, alternative hypotheses, indicators to watch, and action-ready recommendations.
homepage: https://github.com/vassiliylakhonin/global-think-tank-analyst
user-invocable: true
metadata: {"openclaw":{"emoji":"🌍","os":["linux","darwin","win32"]}}
---

# Global Think Tank Analyst

Use this skill for decision-useful analysis of geopolitical, policy, and strategic questions.

## Quick start

Install:

```bash
clawhub install global-think-tank-analyst
```

Run:

```text
think-tank Analyze US-China tech decoupling risks 2026-2030
think-tank --scenarios Arctic resource competition under climate change 2027-2035
think-tank --red-team Russian hybrid tactics in Eastern Europe
```

## Modes

```text
think-tank [topic]
think-tank --report [topic]
think-tank --risk [topic]
think-tank --scenarios [topic] [timeframe]
think-tank --horizon [topic] [timeframe]
think-tank --red-team [claim or policy]
think-tank --json [topic]
```

## Core rules

1. Separate sourced facts from expert judgment.
2. Mark uncertainty explicitly.
3. State key assumptions in deep analysis.
4. Include at least one alternative hypothesis when ambiguity is high.
5. Use a red-team lens to challenge main conclusions.
6. Avoid deterministic language in fast-moving environments.
7. Recommend expert review for crisis or high-stakes decisions.
8. Do not present speculation as fact.

## Decision-grade additions (standard/deep mode)

9. Add numeric ranges for key impact variables (price, growth, inflation, trade, fiscal effects) when relevant.
10. Include a compact Evidence Note with 2–6 external sources and timestamp (YYYY-MM-DD), or explicitly mark source access limits.
11. Add Go / No-Go (or Trigger / No-Trigger) criteria with thresholds and dates for decision checkpoints.
12. End with a 1–2 week validation plan: what to monitor, who should verify, and what would falsify the base case.

## Output contract

Always aim to include:
- Executive summary
- Key assumptions
- Confidence label (High/Medium/Low/Speculative)
- At least one alternative hypothesis when uncertainty is high
- Main risks and indicators to watch
- Action options and recommendations

## Confidence labels

- **High**: well-supported and relatively stable
- **Medium**: plausible but contested or incomplete
- **Low**: weakly supported or rapidly changing
- **Speculative**: forward-looking inference with limited evidence

## Practical guidance

- Separate sourced facts from judgment.
- Do not present speculation as fact.
- Avoid deterministic language in volatile environments.
- Recommend expert review for crisis or high-stakes decisions.

## Optional JSON shape

```json
{
  "query": "",
  "mode": "brief",
  "time_horizon": "",
  "summary": "",
  "drivers": [],
  "risks": [],
  "scenarios": [],
  "policy_options": [],
  "recommendations": [],
  "assumptions": [],
  "alternative_hypotheses": [],
  "confidence": "medium"
}
```
