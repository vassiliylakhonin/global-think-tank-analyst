# Changelog

## Unreleased

- Added `docs/integrations/agenda-intelligence-md.md` — concrete CLI / MCP recipes for composing this skill with Agenda Intelligence MD (markdown score, JSON brief validate+score, evidence-pack audit, MCP loop).
- Added `docs/integrations/agenda-intelligence-md-live-demo.md` — end-to-end run with **real CLI output** (95/100 brief-only → 83/100 with an honest evidence pack), captured against the published Agenda Intelligence MD package on 2026-05-08.
- Added a `live-source-backed` worked example: `examples/live-source-backed-memo.md` (memo on the May 1, 2026 OFAC "Operation Economic Fury" Iran shadow-banking action), paired with a real JSON brief projection and evidence pack under `examples/agenda-projections/`.
- Added three illustrative memos: export-controls exposure, critical-minerals supply-risk, EU energy-transition policy.
- Added a new signal (`signals/2026/2026-05-08.md`) explaining why an honest evidence pack lowers the score.
- Expanded `evals/failure-modes.md` with five new patterns specific to the GTTA + Agenda Intelligence MD composition (score gaming via stripped unsupported claims, JSON projection content loss, mode mismatch on raw markdown scoring, `live_source_backed` claim without an evidence pack, stale `retrieved_at`).
- Trimmed the README Roadmap to reflect what was delivered.

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
