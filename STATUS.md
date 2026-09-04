# Project status

Updated 2026-09-04. Maturity definitions are in
[`docs/maturity-framework.md`](docs/maturity-framework.md); gates for specific
claims are in [`docs/definition-of-done.md`](docs/definition-of-done.md).

## Current coordinates: R2 / M3 / U0

| Axis | Level | Evidence | Next level requires |
|---|---:|---|---|
| Release readiness | R2 | GitHub pre-release `v1.5.0rc1`; source, distribution, and installed-wheel gates; Trusted Publishing workflow on `main` | Restore PyPI account access, register the pending publisher, publish through the protected workflow, and verify installation from PyPI |
| Method evidence | M3 | Four disclosed Markdown runs report 12/12 skill passes vs. 0/12 baseline. The strict MemoArtifact sequence exposed an incomplete adapter, confirmed its correction, and then moved beyond the schema ceiling. The first [declared-behavior run](evals/agent-eval/runs/2026-09-04-antigravity-gemini-3.7-flash-high-artifact-behavior-v1-seed-20260905/) records 12/12 structural passes in both arms and 8/12 skill vs. 3/12 baseline behavioral passes. Exact artifacts, freshness, and limitations are retained. | Replicate the behavior result with another model family and add broader-domain holdouts; practitioner validation remains tracked under U |
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
- The repository has executed and published four controlled 12-case paired
  evaluations under Antigravity: two with Gemini 3.7 Flash (High) and two with
  Claude Opus 4.6 (Thinking). Their deterministic scorer found 12/12 contract
  passes with the skill and 0/12 for the baseline in every run. The fresh
  Claude replication stores 111 skill warnings versus 170 in the prior
  same-ruleset rescore, but cap saturation and sampling variation prevent a
  precise causal interpretation. This is author-operated structural evidence,
  not a factual-quality, decision-quality, or usefulness result.
- The first strict structured-artifact run passed 10/12 baseline samples and
  only 1/12 skill samples. This is evidence of a `1.0.0` output-contract defect,
  not evidence of analytical inferiority: GTTA's human-facing headings were
  not mapped to exact machine keys. A fresh protocol 1.1.0 replication passes
  12/12 in both arms. This confirms the adapter correction for one run but does
  not establish a skill advantage.
- The first preregistered declared-behavior run passed 8/12 skill samples versus
  3/12 baseline samples after both arms passed 12/12 structural checks. The
  observed `+41.7` percentage-point difference applies only to frozen counts
  over declared artifact fields in one Gemini run; it is not a factual,
  analytical-quality, causal, or usefulness result.
- External practitioner usefulness and production reliability are unvalidated.

## Immediate development order

1. Keep `gtta.memo@1.x` and `gtta-method-contract@1.x` stable and testable.
2. Keep the new per-sample truncation telemetry in every published rescore and
   avoid presenting capped warning totals as exact quality deltas.
3. Replicate `gtta-artifact-behavior-eval@1.0.0` with a second model family,
   then use disclosed failures to design a broader-domain holdout without
   rewriting the frozen 12-case benchmark.
4. Complete PyPI Trusted Publishing after account access is restored.
5. Accept practitioner review if access becomes available; do not manufacture a
   substitute metric while the project remains U0.
