# Changelog

## 1.2.0 - 2026-05-08

- Repositioned README, AGENTS.md, llms.txt, SKILL.md, and codex/SKILL.md to frame the project as a **strategic-risk analysis skill for AI agents**, distinct from the companion infrastructure project Agenda Intelligence MD.
- Replaced AGENTS.md with the canonical project-rules spec: project identity, honesty rules, evidence rules, recommended README structure, naming hierarchy, and definition of done.
- Renamed "Output modes" to "Memo modes" and reordered the README to recommended structure (quick usage → memo modes → before/after → examples → evals → signal archive → limitations → roadmap).
- Added `examples/` with four illustrative memos (sanctions exposure, regulatory impact, scenario brief, red-team), all explicitly labeled `reasoning-only / illustrative`.
- Added `evals/` with a human review checklist, failure-modes catalogue, and starter scoring rubric.
- Added `signals/TEMPLATE.md` and reframed the signal archive as public examples of the skill style, not official intelligence.
- Added explicit Limitations and Roadmap sections.
- Added an integration status table that separates implemented from compatible from not-implemented.
- Tightened naming hierarchy: Product = Global Think Tank Analyst; Method = Policy Risk Memo Architect; Companion = Agenda Intelligence MD.
- Backfilled evidence-mode and confidence headers on the existing 2026-04-28 signal.

## 1.1.0 - 2026-05-06

- Repositioned the project from an OpenClaw/Codex-centered skill to a universal AI-agent playbook.
- Added `AGENTS.md` with runtime-neutral instructions for ChatGPT, Claude, Gemini, Perplexity, Cursor, Codex, OpenClaw, MCP agents, RAG systems, and internal copilots.
- Added Decision Briefing Pack mode for team-facing decisions, owners, watchlists, triggers, and review cadence.
- Expanded README, `llms.txt`, and skill guidance with stronger user-facing integration paths and clearer evidence discipline.

## 1.0.1 - 2026-04-17

- Reduced package to minimal skill content for ClawHub release hygiene.
- Kept core `SKILL.md` aligned with Policy Risk Memo Architect framing.

## 1.0.0 - 2026-04-17

- Major rewrite and repositioning to **Policy Risk Memo Architect**.
- Added stronger evidence-discipline guardrails.
- Added clearer output modes and decision-oriented default template.
