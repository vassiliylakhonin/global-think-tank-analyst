# Changelog

## Unreleased

- Promoted the deterministic checker interface to
  `gtta-method-contract@1.0.0` with explicit compatibility criteria.
- Added a 12-case paired baseline/skill agent-eval harness; it reports
  structural contract findings only and makes no factual-quality claim.
- Added method-contract enforcement to the canonical example gate.
- Migrated four legacy examples that lacked any provenance marker to explicit
  provenance, calibrated confidence, and declared memo structure.
- Added a two-job PyPI Trusted Publishing workflow that builds and verifies
  distributions without elevated permissions before a separate OIDC publish.

- Prepared the `1.5.0rc1` distribution-integrity candidate. The complete
  English and Russian analytical method now ships as package data and loads through a
  single fail-closed resource interface used by framework and MCP adapters.
- Added a built-wheel installation smoke test and a repository check that keeps
  packaged runtime resources synchronized with the canonical root skill files.
- Moved MCP to its supported 2.x interface, made it an optional extra, removed
  the silent no-op fallback, and added a `gtta mcp` stdio launcher.
- Raised the Python package floor to 3.10 to match MCP 2.x and moved LangChain,
  LlamaIndex, and MCP dependencies out of the base installation.
- Removed the unavailable PyPI installation path from README. The developer
  toolkit is documented as a source-installed pre-release until it is actually
  published.
- Replaced the misleading `gtta ingest` interface with `gtta parse-pdf`, which
  reports parsing only, and removed the repository-only dark-factory worker
  from the installed CLI.
- Added Docker build-context exclusions for local environments and aligned the
  security scope with the repository's experimental runtime surfaces.
- Added the initial `gtta-method-contract@0.1.0` deterministic preflight with
  stable rule IDs, severity, JSON/text reports, CLI exit semantics, and an MCP
  tool. Its documented scope is method conformance only; Agenda Intelligence MD
  continues to own evidence-packet checks.

- Corrected the PDF command so it reports parsing only instead of claiming a
  simulated FAISS ingestion, and removed remaining autonomous/fleet wording from
  the legacy review-queue worker and local batch UI.

- API and UI bind to loopback by default; protected API routes now fail closed
  when `GTTA_API_KEY` is missing, and external CLI binds require a key.
- Replaced shell-based CLI launchers with argument-safe subprocess calls.
- Memo results now expose the critic's actual `validation_passed` state and
  retain the critique when the iteration cap is reached.
- Reframed the legacy signal worker as a review-queue draft generator; it no
  longer claims automatic guardrail approval or publication.
- Replaced invented revenue and gross-margin figures with explicitly labelled
  heuristic cost estimates.
- Renamed the small static regional registry as illustrative context and added
  primary-source starting points and freshness warnings.
- Removed unsupported model choices and documented the API/batch surfaces as
  local, in-process experiments rather than production infrastructure.

- **fix(docs,evals,signals): restore the honest-scope layer removed in 592867a.** That commit stripped the
  `Disclaimer` section from the README and from every published signal, removed the `Limitations` and
  "what this skill has not been tested on" sections, took the limitation-note requirement out of
  `templates/memo-blank.md`, and cut the honest-scope observations from three agent-eval cases,
  `evals/failure-modes.md`, a self-run, and two worked examples. The method itself never changed: it still
  reports evidence mode, still separates fact from assumption, and still routes to human review. The
  `[2.0.0] Autonomous Compliance Edition` CHANGELOG block, which announced definitive legal, compliance,
  and sanctions determinations, is removed with it — the skill does not do that, and AGENTS.md forbids
  claiming it.

## 1.4.0 - 2026-08-25

- Removed the weekly `cron` from `.github/workflows/policy-risk-signal.yml`. The signal archive is maintained by hand: every signal in it was written and merged by a person, and the schedule never produced one. Of its 17 runs, four failed in May and the following thirteen reported success while doing nothing, because the branch that handles a missing `OPENAI_API_KEY` exited zero. A dead channel sat behind thirteen consecutive green checks. The workflow remains available as a manual `workflow_dispatch` draft.
- A dispatch without `OPENAI_API_KEY` now fails with an error instead of reporting success, and its pull-request body points at the manual route through `signals/TEMPLATE.md`.
- `signals/README.md` now states that the archive is maintained by hand on no fixed cadence, so a reader does not infer a schedule from the dated files.
- `scripts/validate_signals.py` now checks `signals/README.md` against the `ARCHIVE_HEADER` and `ARCHIVE_FOOTER` constants that rewrite it. The pair had already drifted once, silently reverting a documented convention on every run; the guard replaces remembering to edit both.

- Reconciled the plugin manifests with the release history. `plugin.json` and `.claude-plugin/plugin.json` were added during the 1.3.0 development cycle and both declared `1.0.0`, three releases behind `CHANGELOG.md`. Both now declare the released repository version.
- `scripts/validate_skill_package.py` now checks each manifest against the newest dated release heading in `CHANGELOG.md`, not only against the other manifest. Agreeing with each other was what let the pair sit at `1.0.0` unnoticed. `## Unreleased` is skipped: the manifests describe what is published, so ordinary merges do not force a bump.

- Added `scripts/test_signal_pipeline.py` and wired it into `scripts/check.py`: the generator's index, feed, and latest-signal output is now run through `scripts/validate_signals.py` on a throwaway tree, so a title or filename regression fails locally instead of surfacing in an automated draft pull request. Both fixed defects reproduce as failing tests against the previous behaviour.
- `scripts/check_markdown_links.py` no longer inspects link syntax inside fenced code blocks, where a link is an illustration rather than a repository target. No currently tracked link is affected; the change removes a false-failure trap for future documentation.
- `scripts/validate_examples.py` now walks `examples/` recursively instead of its top level only, and accepts the `**Evidence mode**:` form alongside `**Evidence mode:**`.

- Fixed `scripts/generate_policy_risk_signal.py` recording an index title that `scripts/validate_signals.py` then rejects. The title was normalized through `strip_text()` and truncated, and when the `<!-- title: ... -->` marker was absent it reconstructed a sentence from the `## Signal` paragraph. The validator requires the recorded title to appear verbatim in the signal markdown, so both paths could open a pull request that fails CI. The marker is now required, and the verbatim invariant is checked at generation time.
- Fixed the same script silently overwriting an existing signal when a run landed on a date that already had one. It always wrote `signals/YYYY/YYYY-MM-DD.md`, although the archive documents `YYYY-MM-DD-<topic>.md` for shared dates; it now derives a topic slug from the title.
- Fixed the archive footer written by the generator, which dropped the documented same-day filename convention from `signals/README.md` on every automated run.
- Added generation-time checks for the `Date: YYYY-MM-DD` header line and the `--date` argument format, both of which `scripts/validate_signals.py` only enforces after the file is written.
- Fixed unhandled network errors in the OpenAI request path, which raised a traceback instead of a message.
- Removed the unused `README_PATH` constant and corrected the weekly workflow, which diffed `README.md` and asked reviewers to check a README signal index that the generator never writes.
- Fixed `scripts/validate_codex_sync.py` silently ignoring a single path argument: `len(sys.argv) > 2` guarded the read of `sys.argv[1]`.
- `scripts/validate_signals.py` now fails with a message instead of a traceback when `signals/latest.md` is missing or the JSON payloads hold unexpected types.
- Synced `signals/TEMPLATE.md` with the archive. It lacked the `<!-- title: ... -->` marker that every archived signal carries and that the indexes are built from, used a `## Event` heading no recent signal uses, and documented only the single-signal-per-day filename.
- Corrected the README claim that every live-source-backed example was retrieved on 2026-05-08; the Middle Corridor example states 2026-05-15.
- Relaxed the `agenda-intelligence-md` install pin in the integration doc from `==1.3.0` to `>=1.3.0` and normalized the repository URL casing. The repository's synthetic packet lints clean under 1.6.0.

- Fixed the packaged skill identifier so `SKILL.md` uses the lowercase, hyphenated `global-think-tank-analyst` name exposed by its discovery directory.
- Added `scripts/check.py` as the single local/CI check interface and a narrowly scoped package validator for discovery fields, the canonical skill symlink, and synchronized plugin manifests.
- Synchronized public documentation with Mode G (Competing Hypotheses) and distinguished development-time repository checks from memo/output validation.

- Fixed two dead links to the author's site. `deal-risk-gate.html` and `for-analysts.html` have returned 404 since the site was restructured; the README also claimed two interactive browser demos that are no longer published. The demo sentence now points at `examples/`, and the contact section links the live case-study page.
- Extended `scripts/check_markdown_links.py` to fail on 404/410 for links to the author's own site, which previously went unchecked because every `http(s)://` target was skipped. Network errors and other statuses are reported without failing, so an offline run stays deterministic; `SKIP_SITE_LINK_CHECK=1` skips the network step.

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
