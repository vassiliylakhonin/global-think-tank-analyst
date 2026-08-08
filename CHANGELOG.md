# Changelog

## Unreleased

- Conformed the repo to the Agent Plugins 1.0.0 layout: added a root `plugin.json` with the `$schema` identifier from <https://agent-plugins.org>. `.claude-plugin/plugin.json` is unchanged and still serves the Claude Code install path; the specification ignores that directory. `skills/global-think-tank-analyst/SKILL.md` already matched the spec's discovery rule. The manifest validates against the published Draft 2020-12 schema.

- Added the Agenda Intelligence v1.3 evidence-packet handoff as the primary composition seam, with a runnable synthetic packet, dependency-free CI validator, and ADR 0001. Reclassified older memo-schema, scoring, `analyze`, and MCP recipes as compatibility workflows.

- Packaged the repo as an installable Claude Code plugin: added `.claude-plugin/plugin.json` and `skills/global-think-tank-analyst/SKILL.md` (a symlink to the canonical root `SKILL.md`; packaging only, not a runtime overlay). Installable via `/plugin marketplace add vassiliylakhonin/agenda-intelligence-md`, then `/plugin install global-think-tank-analyst@agenda-intelligence`. Verified locally with `claude plugin install` from an isolated config (1 skill discovered via the symlink).

- Clarified the commercial role: this repo remains the horizontal reasoning-method dependency behind Agenda Intelligence MD, not a buyer-facing product surface. Added README/AGENTS guidance to route product positioning and evidence-readiness commercialization through Agenda Intelligence MD.
- Added `scripts/validate_codex_sync.py` and wired it into CI: fails the build when the shared analytical contract in `codex/SKILL.md` drifts from the canonical root `SKILL.md`. Intentional codex-only / divergent sections are allowlisted in the script. Enforces the manual sync discipline declared in codex/SKILL.md's Contract provenance section.
- Resynced `codex/SKILL.md` shared analytical contract with the canonical root `SKILL.md`: restored the `Stop and request — explicit triggers` subsection, restored two dropped self-check items (provenance-language match, conflict-surfacing), and reverted three paraphrased contract paragraphs (retrieved-content trust, conflict handling, linguistic faithfulness) to the canonical root wording. Intentional codex-only sections (Contract provenance, Codex Platform Setup, JSON Output Mode, Pipeline Integration, the Mode F agentic-loop note, and Installation) are unchanged.
- Spawned three signals from existing live-source-backed memos: Hormuz oil-price corridor, EU AI Act simplification redeployment, China critical-minerals procurement window. Hardened the signal-generation script to support `YYYY-MM-DD-<topic>.md` filenames so multiple signals can share a date.
- Added two more `live-source-backed` worked examples: ECB rate-hold (2026-04-30, ECB primary publications) and EU CBAM enforcement-phase exposure (2026 definitive phase, DG TAXUD).
- Converted the README example list to a domain × evidence-mode matrix for navigation.
- Added ECB and BIS feeds to `.github/policy-risk-signal/sources.json` to broaden monetary-policy and financial-stability coverage in the auto-signal pipeline.

## 1.3.0 - 2026-05-09

- Added `docs/integrations/agenda-intelligence-md.md` — concrete CLI / MCP recipes for composing this skill with Agenda Intelligence MD (markdown score, JSON brief validate+score, evidence-pack audit, MCP loop).
- Added `docs/integrations/agenda-intelligence-md-live-demo.md` — end-to-end run with **real CLI output** (95/100 brief-only → 83/100 with an honest evidence pack), captured against the published Agenda Intelligence MD package on 2026-05-08.
- Added a `live-source-backed` worked example: `examples/live-source-backed-memo.md` (memo on the May 1, 2026 OFAC "Operation Economic Fury" Iran shadow-banking action), paired with a real JSON brief projection and evidence pack under `examples/agenda-projections/`.
- Added three illustrative memos: export-controls exposure, critical-minerals supply-risk, EU energy-transition policy.
- Added a new signal (`signals/2026/2026-05-08.md`) explaining why an honest evidence pack lowers the score.
- Expanded `evals/failure-modes.md` with five new patterns specific to the GTTA + Agenda Intelligence MD composition (score gaming via stripped unsupported claims, JSON projection content loss, mode mismatch on raw markdown scoring, `live_source_backed` claim without an evidence pack, stale `retrieved_at`).
- Added three additional `live-source-backed` worked examples (real sources retrieved 2026-05-08): Hormuz disruption / energy prices, EU AI Act simplification (Omnibus VII), and the China critical-minerals export-control suspension.
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
