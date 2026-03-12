# Global Think-Tank Analyst (OpenClaw Skill)

<p align="left">
  <a href="https://github.com/vassiliylakhonin/global-think-tank-analyst/stargazers"><img src="https://img.shields.io/github/stars/vassiliylakhonin/global-think-tank-analyst?style=for-the-badge" alt="Stars"></a>
  <a href="https://github.com/vassiliylakhonin/global-think-tank-analyst/network/members"><img src="https://img.shields.io/github/forks/vassiliylakhonin/global-think-tank-analyst?style=for-the-badge" alt="Forks"></a>
  <a href="https://github.com/vassiliylakhonin/global-think-tank-analyst/issues"><img src="https://img.shields.io/github/issues/vassiliylakhonin/global-think-tank-analyst?style=for-the-badge" alt="Issues"></a>
  <a href="https://github.com/vassiliylakhonin/global-think-tank-analyst/commits/main"><img src="https://img.shields.io/github/last-commit/vassiliylakhonin/global-think-tank-analyst?style=for-the-badge" alt="Last Commit"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License"></a>
</p>

A decision-grade policy analysis skill for OpenClaw that helps teams produce **structured, evidence-aware, and implementation-ready** briefs in the style of leading global think tanks.

Designed for policy, strategy, and research workflows where outputs must be useful for real decisions—not just descriptive summaries.

---

## Why this skill exists

Most AI outputs on policy are either:
- too generic to guide decisions, or
- too verbose to be operational.

This skill is built to close that gap by enforcing:
- clear decision objectives,
- explicit assumptions,
- option comparison with trade-offs,
- risk ownership,
- and execution pathways.

---

## Core capabilities

- Decision-focused policy briefs (not generic summaries)
- Scenario analysis (best/base/worst + trigger indicators)
- Stakeholder and political-economy mapping
- Policy option comparison with feasibility and time-to-impact
- Risk register with mitigation owners
- Implementation pathways (30/60/90 + 4–12 month horizon)
- Explicit assumptions, evidence quality, and confidence labels

---

## Best fit use cases

- Government and ministerial advisory memos
- Think tank and policy unit analysis
- NGO/donor strategy notes
- Geopolitical and public policy scenario planning
- Institution-facing AI workflows requiring auditability

---

## Install

```bash
clawhub install global-think-tank-analyst
```

Install a pinned version:

```bash
clawhub install global-think-tank-analyst --version 1.0.0
```

---

## Quick start

Use in OpenClaw:

```text
Use $global-think-tank-analyst to evaluate policy options for [topic], including stakeholder analysis, scenarios, risks, and implementation pathways.
```

Example prompt:

```text
Use $global-think-tank-analyst to assess policy options for regulating frontier AI models in Central Asia over the next 24 months. Include a stakeholder map, scenario analysis, and a 30/60/90-day implementation plan.
```

---

## Output structure (typical)

1. Executive Summary  
2. Policy Objective  
3. Current Context  
4. Stakeholder Map  
5. Policy Options and Trade-offs  
6. Scenario Analysis  
7. Risk Register  
8. Implementation Pathway  
9. Monitoring Framework  
10. Final Recommendation  
11. Assumptions, Evidence Quality, Confidence

---

## Quality standards

- **Decision usefulness over verbosity**
- **Transparent assumptions and uncertainty**
- **Operational realism (budget/legal/political constraints)**
- **Actionable recommendations with clear next steps**

---

## Contributing

Contributions are welcome.

Suggested contributions:
- Improve prompt patterns and examples
- Add domain-specific policy templates
- Tighten quality gates for high-stakes topics
- Improve clarity and brevity of output structures

Open an issue first for substantial changes so we can align scope.

---

## Repository purpose

This repository packages a reusable OpenClaw skill for policy and strategic analysis where quality must be practical, evidence-aware, and implementation-ready.

## License

MIT
