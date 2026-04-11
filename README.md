# Global Think Tank Analyst

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Forks](https://img.shields.io/github/forks/vassiliylakhonin/global-think-tank-analyst?style=flat)](https://github.com/vassiliylakhonin/global-think-tank-analyst/forks)
[![Stars](https://img.shields.io/github/stars/vassiliylakhonin/global-think-tank-analyst?style=flat)](https://github.com/vassiliylakhonin/global-think-tank-analyst/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/vassiliylakhonin/global-think-tank-analyst)](https://github.com/vassiliylakhonin/global-think-tank-analyst/commits/main)

Decision-grade geopolitical and policy analysis skill for OpenClaw/ClawHub.

**What you get:** concise thesis, assumptions, confidence, alternative hypotheses, risks, scenarios, and action-ready recommendations.

---

## Why this is different

Most analysis prompts produce long text.
This skill produces **decision memos**.

- Explicit assumptions
- Confidence labels + scoring rubric
- Competing hypotheses + red-team checks
- Trigger-based Go / No-Go logic
- 1–2 week validation plan
- Subagent-ready orchestration for deep workflows

---

## Quick start

```bash
clawhub install global-think-tank-analyst
```

```text
think-tank Analyze US-China tech decoupling risks 2026-2030
think-tank --scenarios Arctic resource competition 2027-2035
think-tank --red-team "EU strategic autonomy is realistic by 2030"
```

---

## Modes

- `think-tank [topic]` - concise brief
- `think-tank --report [topic]` - full structured report
- `think-tank --risk [topic]` - risk matrix + triggers + impacts
- `think-tank --scenarios [topic] [timeframe]` - baseline/optimistic/pessimistic/wildcard
- `think-tank --horizon [topic] [timeframe]` - weak signals + wildcards
- `think-tank --red-team [claim]` - challenge assumptions and failure modes
- `think-tank --json [topic]` - machine-readable output

---

## See a real output

- **Sample memo:** [examples/decision-memo-sample.md](./examples/decision-memo-sample.md)
- **Prompt pack:** [examples/queries.md](./examples/queries.md)

---

## Fork this in 15 minutes

If you want your own niche version, start here:

- **Guide:** [FORK_GUIDE.md](./FORK_GUIDE.md)
- **Adaptation ideas:** [examples/adaptations.md](./examples/adaptations.md)

Typical fork directions:

1. Government risk desk
2. Startup/VC strategy analyst
3. Nonprofit policy-impact analyst
4. Regional security analyst
5. Supply-chain geopolitical monitor

---

## Project structure

```text
.
├── SKILL.md
├── README.md
├── FORK_GUIDE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── examples/
└── references/
```

Advanced references:
- `references/subagent-orchestration.md`
- `references/confidence-rubric.md`
- `references/eval-pack.md`

---

## Contributing

PRs and forks are welcome.

- Contribution guide: [CONTRIBUTING.md](./CONTRIBUTING.md)
- If you fork and adapt it, open an issue with your version so it can be featured.

---

## License

MIT
