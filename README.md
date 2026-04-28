# Policy Risk Memo Architect

[![ClawHub](https://img.shields.io/badge/ClawHub-global--think--tank--analyst-2bc6a4)](https://clawhub.ai/vassiliylakhonin/global-think-tank-analyst)
[![CI](https://github.com/vassiliylakhonin/global-think-tank-analyst/actions/workflows/ci.yml/badge.svg)](https://github.com/vassiliylakhonin/global-think-tank-analyst/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Decision-ready geopolitical, policy, sanctions, trade, regulatory, and strategic-risk memos for OpenClaw and Codex.**

Policy Risk Memo Architect turns broad risk questions into structured analysis with explicit evidence limits, uncertainty labels, competing interpretations, practical options, and indicators to watch. It is designed for users who need a usable decision memo, not a decorative geopolitical essay.

## Why this skill exists

Most AI policy analysis fails in predictable ways: it overstates certainty, buries the decision, mixes facts with speculation, and produces polished background instead of usable judgment.

This skill enforces a stricter memo discipline:

- define the decision problem before analyzing it;
- separate **facts**, **assumptions**, **assessments**, **scenarios**, and **unknowns**;
- expose evidence limits instead of hiding them;
- present competing interpretations when ambiguity matters;
- end with options, trade-offs, indicators, and bounded confidence.

## Best for

- country risk briefs;
- sanctions and export-control exposure assessments;
- trade, tariff, and regulatory impact memos;
- geopolitical scenario briefs;
- stakeholder and incentives analysis;
- red-team challenges to an existing policy or risk view;
- leadership-facing strategic implications notes.

## Not for

- legal advice;
- intelligence-style certainty;
- generic news summaries;
- academic literature reviews;
- unsupported numerical forecasting;
- prestige-sounding analysis with weak evidence.

## Output modes

| Mode | Use when you need | Typical output |
|---|---|---|
| **A — Quick Brief** | Fast orientation | Bottom line, why it matters, main risks, watchlist, confidence |
| **B — Standard Memo** | Default decision memo | Executive takeaway, context, evidence limits, actors, assessment, options |
| **C — Scenario Brief** | Divergent futures matter | Baseline, 2–4 scenarios, triggers, implications, indicators |
| **D — Red-Team Challenge** | Stress-test a claim | Failure modes, alternative explanations, missing assumptions, revised judgment |

## What the memo always makes explicit

| Standard | How it appears |
|---|---|
| Decision framing | `Question`, `Decision`, `Audience`, `Time horizon`, `Evidence mode` |
| Evidence discipline | `Fact`, `Assessment`, `Assumption`, `Scenario`, `Unknown` labels |
| Evidence limits | Required notice when live/source verification was not performed |
| Uncertainty | `Low`, `Moderate`, or `High` confidence tied to evidence quality |
| Practical relevance | Options, trade-offs, implementation friction, and indicators to watch |

## Policy Risk Signal — 7 days of signals → decision memos

Short, source-aware policy risk notes showing how this skill turns public signals into decision-ready analysis.

- [2026-04-28](signals/2026/2026-04-28.md): Evidence discipline is the product, not decoration

[Full signal archive →](signals)

## Automated signal pipeline

The repository includes a weekly GitHub Actions pipeline that drafts the next Policy Risk Signal from public RSS/Atom sources and opens a pull request for review.

How it works:

1. Fetch public source snippets from `.github/policy-risk-signal/sources.json`.
2. Generate one short source-aware signal with `scripts/generate_policy_risk_signal.py`.
3. Write `signals/YYYY/YYYY-MM-DD.md` and update the README/archive indexes.
4. Open a pull request instead of publishing directly to `main`.

Required setup:

- add repository secret `OPENAI_API_KEY`;
- optionally set repository variable `OPENAI_MODEL`;
- run the **Policy Risk Signal** workflow manually once, then let the weekly schedule continue.

The review step is intentional: policy-risk content should be checked before publication.

Agent-readable endpoints:

- [`llms.txt`](llms.txt) — quick orientation for LLMs and agents;
- [`signals/latest.md`](signals/latest.md) — latest signal in markdown;
- [`signals/index.json`](signals/index.json) — machine-readable signal index;
- [`signals/feed.json`](signals/feed.json) — JSON Feed for automated ingestion.

## Installation

```bash
openclaw skills install vassiliylakhonin/global-think-tank-analyst
```

Then ask OpenClaw for a policy-risk memo, scenario brief, or red-team challenge. The skill will activate when the request matches its domain.

## Codex usage

A Codex-ready variant is included at:

```text
codex/SKILL.md
```

Use that file in Codex skill workflows when you want the same analytical standard outside OpenClaw.

## Example prompts

### Mode A — Quick Brief

```text
Prepare a quick brief on EU CBAM exposure for a Kazakh metals exporter over the next 12 months.
```

### Mode B — Standard Memo

```text
Write a policy-risk memo on sanctions exposure for a Russian energy company operating in Central Asia.
```

### Mode C — Scenario Brief

```text
Provide a scenario brief on possible US-China semiconductor control developments for 2026-2028.
```

### Mode D — Red-Team Challenge

```text
Red-team the claim that supply-chain sanctions risk for a European technology firm is manageable.
```

## Recommended prompt shape

For best results, include the decision context:

```text
Use Policy Risk Memo Architect.
Question: ...
Decision this informs: ...
Audience: ...
Geography: ...
Time horizon: ...
Evidence mode: source-backed / reasoning-only / mixed
Depth: quick brief / standard memo / scenario brief / red-team
```

If you do not provide all fields, the skill will infer what it can and state assumptions.

## Repository structure

```text
.
├── SKILL.md              # OpenClaw skill
├── codex/SKILL.md        # Codex-ready variant
├── README.md             # Public documentation
├── signals/              # Weekly Policy Risk Signal archive
├── scripts/              # Signal generation automation
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
└── .github/              # CI, issue templates, PR template
```

## Trust and safety posture

This skill is intentionally conservative about evidence. It should not fabricate sources, imply live verification when none occurred, or present speculative geopolitical judgments as facts.

It is a decision-support tool, not legal, compliance, investment, or intelligence advice.

## License

MIT — see [LICENSE](LICENSE).
