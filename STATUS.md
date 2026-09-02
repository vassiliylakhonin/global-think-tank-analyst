# Project status

Updated 2026-09-02. Maturity definitions are in
[`docs/maturity-framework.md`](docs/maturity-framework.md); gates for specific
claims are in [`docs/definition-of-done.md`](docs/definition-of-done.md).

## Current coordinates: R2 / M3 / U0

| Axis | Level | Evidence | Next level requires |
|---|---:|---|---|
| Release readiness | R2 | GitHub pre-release `v1.5.0rc1`; source, distribution, and installed-wheel gates; Trusted Publishing workflow on `main` | Restore PyPI account access, register the pending publisher, publish through the protected workflow, and verify installation from PyPI |
| Method evidence | M3 | Four disclosed 12-case Antigravity runs: two Gemini and two Claude. All report 12/12 contract passes with the skill vs. 0/12 for the baseline. The first Claude run stores 170 skill warnings under 1.2.2 and the fresh [post-change replication](evals/agent-eval/runs/2026-09-01-antigravity-claude-opus-4.6-thinking-seed-20260902/) stores 111. Ruleset 1.2.3 shows those arms contain 2 and 3 truncated samples respectively, so totals are lower bounds. Exact artifacts, freshness comparisons, triage, and limitations are published. | Execute the implemented structured-artifact path, then broaden task domains; practitioner validation remains tracked under U |
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
- External practitioner usefulness and production reliability are unvalidated.

## Immediate development order

1. Keep `gtta.memo@1.x` and `gtta-method-contract@1.x` stable and testable.
2. Keep the new per-sample truncation telemetry in every published rescore and
   avoid presenting capped warning totals as exact quality deltas.
3. Execute and publish the first structured `MemoArtifact` paired run, then
   version a broader task suite without rewriting the frozen 12-case benchmark.
4. Complete PyPI Trusted Publishing after account access is restored.
5. Accept practitioner review if access becomes available; do not manufacture a
   substitute metric while the project remains U0.
