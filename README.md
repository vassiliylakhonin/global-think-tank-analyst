# Global Think Tank Analyst (OpenClaw Skill)

`global-think-tank-analyst` produces structured geopolitical, strategic, and policy analysis in a clear think-tank style.

It is designed for decision-useful outputs with explicit assumptions, confidence labels, alternative hypotheses, and practical recommendations.

## What this skill does

- Builds executive policy briefs and full strategic reports
- Produces risk assessments, horizon scans, and scenario sets
- Maps actors, incentives, constraints, and power balances
- Stress-tests claims with red-team and alternative-hypothesis logic
- Exports structured JSON for downstream workflows

## Install

```bash
clawhub install global-think-tank-analyst
```

## Quick usage

```text
think-tank Analyze US-China tech decoupling risks 2026–2030
```

```text
think-tank --scenarios Arctic resource competition under climate change 2027–2035
```

```text
think-tank --red-team Russian hybrid tactics in Eastern Europe
```

## Common modes

- `think-tank [topic]` — concise brief
- `think-tank --report [topic]` — full structured report
- `think-tank --risk [topic]` — exposure, triggers, impact pathways
- `think-tank --scenarios [topic] [timeframe]` — plausible futures + signposts
- `think-tank --horizon [topic] [timeframe]` — emerging signals and wildcards
- `think-tank --red-team [claim or policy]` — stress-test assumptions and conclusions
- `think-tank --json [topic]` — structured machine-readable output

## Typical outputs

1. Executive summary + situation overview
2. Strategic drivers and context scan
3. Actor map / stakeholder analysis
4. Risk matrix and trigger indicators
5. Baseline / optimistic / pessimistic / wildcard scenarios
6. Options, recommendations, and indicators to watch
7. Confidence labels, assumptions, and alternative hypotheses

## Repository structure

```text
.
├── SKILL.md
├── README.md
└── LICENSE
```

## License

MIT
