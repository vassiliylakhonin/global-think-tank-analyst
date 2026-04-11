# Global Think Tank Analyst (OpenClaw Skill)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Fork this repo](https://img.shields.io/badge/Fork-friendly-blue.svg)](./FORK_GUIDE.md)
[![Contributions welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

Decision-grade geopolitical, strategic, and policy analysis for OpenClaw/ClawHub.

## Why people fork this skill

- Clear analysis contract (assumptions, confidence, alternatives)
- Reusable output structure for different domains
- Easy adaptation path in under 15 minutes

## Quick Start

```bash
clawhub install global-think-tank-analyst
```

```text
think-tank Analyze US-China tech decoupling risks 2026-2030
think-tank --scenarios Arctic resource competition under climate change 2027-2035
think-tank --red-team Russian hybrid tactics in Eastern Europe
```

## Fork and adapt in 15 minutes

Read: **[FORK_GUIDE.md](./FORK_GUIDE.md)**

Typical fork paths:
- Government policy risk desk
- Startup/VC strategy analyst
- Nonprofit impact/policy analyst

## What to change after forking

1. `SKILL.md` frontmatter (`name`, `description`, `homepage`)
2. Domain focus + frameworks in `SKILL.md`
3. README positioning and examples
4. Add your domain prompts in `examples/`

## Common modes

- `think-tank [topic]` - concise brief
- `think-tank --report [topic]` - full structured report
- `think-tank --risk [topic]` - exposure, triggers, impact pathways
- `think-tank --scenarios [topic] [timeframe]` - plausible futures + signposts
- `think-tank --horizon [topic] [timeframe]` - emerging signals and wildcards
- `think-tank --red-team [claim or policy]` - challenge assumptions and conclusions
- `think-tank --json [topic]` - structured machine-readable output

## Example prompts

- See **[examples/queries.md](./examples/queries.md)**
- Adaptation ideas: **[examples/adaptations.md](./examples/adaptations.md)**

## Contributing

Please read **[CONTRIBUTING.md](./CONTRIBUTING.md)**.

## Changelog

See **[CHANGELOG.md](./CHANGELOG.md)**.

## License

MIT
