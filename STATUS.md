# Project status

Updated 2026-08-31. Maturity definitions are in
[`docs/maturity-framework.md`](docs/maturity-framework.md); gates for specific
claims are in [`docs/definition-of-done.md`](docs/definition-of-done.md).

## Current coordinates: R2 / M3 / U0

| Axis | Level | Evidence | Next level requires |
|---|---:|---|---|
| Release readiness | R2 | GitHub pre-release `v1.5.0rc1`; source, distribution, and installed-wheel gates; Trusted Publishing workflow on `main` | Restore PyPI account access, register the pending publisher, publish through the protected workflow, and verify installation from PyPI |
| Method evidence | M3 | Three disclosed 12-case Antigravity runs: two with Gemini 3.7 Flash (High) and one freshness-gated [Claude Opus 4.6 cross-model run](evals/agent-eval/runs/2026-08-31-antigravity-claude-opus-4.6-thinking-seed-20260901/). All report 12/12 contract passes with the skill vs. 0/12 for the baseline. The Claude skill arm reports 181 capped warnings under its original ruleset and 170 under the narrow 1.2.2 precision rescore, exposing weaker per-claim provenance transfer. Exact inputs, outputs, hashes, recorded settings, reports, triage, and limitations are published. | Repeat across the second model family after runtime-method changes and broaden task domains; practitioner validation remains tracked under U |
| External usefulness | U0 | No external practitioner review record exists; `reviews/` contains scaffolding only | One real review reaches U1; two independent relevant reviews with recorded findings reach U2 |

## Release state

- Latest GitHub candidate: `v1.5.0rc1`.
- Development version on `main`: `1.6.0.dev0`.
- PyPI publication is blocked by account recovery / two-factor access, not by a
  source or CI failure.
- The release candidate remains an honest GitHub pre-release while that access
  issue is unresolved.

## Claims currently allowed

- GTTA is an experimental, testable strategic-risk reasoning framework.
- Its package, CLI, MCP adapter, method checker, and structured memo artifact
  have automated conformance tests.
- The repository has executed and published three controlled 12-case paired
  evaluations under Antigravity: two with Gemini 3.7 Flash (High) and one with
  Claude Opus 4.6 (Thinking). Their deterministic scorer found 12/12 contract
  passes with the skill and 0/12 for the baseline in every run. The Claude run
  repeats the pass delta across a second model family but also reports 181
  capped skill warnings in the immutable original report and 170 under the
  1.2.2 precision rescore. This is author-operated structural evidence, not a
  factual-quality, decision-quality, or usefulness result.
- External practitioner usefulness and production reliability are unvalidated.

## Immediate development order

1. Keep `gtta.memo@1.x` and `gtta-method-contract@1.x` stable and testable.
2. Preserve the Claude `1.2.1` run and its separate `1.2.2` rescore; tighten
   runtime instructions for canonical per-claim provenance and explicit Mode C
   triggers without relaxing valid findings.
3. Repeat the Claude-family run on fresh outputs after the runtime change,
   then broaden task domains.
4. Complete PyPI Trusted Publishing after account access is restored.
5. Accept practitioner review if access becomes available; do not manufacture a
   substitute metric while the project remains U0.
