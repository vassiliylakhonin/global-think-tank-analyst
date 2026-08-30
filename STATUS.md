# Project status

Updated 2026-08-30. Maturity definitions are in
[`docs/maturity-framework.md`](docs/maturity-framework.md); gates for specific
claims are in [`docs/definition-of-done.md`](docs/definition-of-done.md).

## Current coordinates: R2 / M3 / U0

| Axis | Level | Evidence | Next level requires |
|---|---:|---|---|
| Release readiness | R2 | GitHub pre-release `v1.5.0rc1`; source, distribution, and installed-wheel gates; Trusted Publishing workflow on `main` | Restore PyPI account access, register the pending publisher, publish through the protected workflow, and verify installation from PyPI |
| Method evidence | M3 | [Disclosed 12-case (24-sample) paired evaluation](evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high/) executed in Antigravity with Gemini 3.7 Flash (High), seed 20260830: 12/12 contract passes with the skill vs. 0/12 for the baseline; exact inputs, outputs, hashes, settings, and limitations published | Broaden evaluation across independent model families and task domains; practitioner validation remains tracked under U |
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
- The repository has executed and published a controlled 12-case paired
  evaluation under Antigravity with Gemini 3.7 Flash (High). Its deterministic
  scorer found 12/12 contract passes with the skill and 0/12 for the baseline.
  This is structural evidence, not a factual-quality or usefulness result.
- External practitioner usefulness and production reliability are unvalidated.

## Immediate development order

1. Keep `gtta.memo@1.x` and `gtta-method-contract@1.x` stable and testable.
2. Replicate M3 across independent model families and address the 25 actionable
   GTTA010 findings isolated by the `1.2.0` frozen-output rescore.
3. Complete PyPI Trusted Publishing after account access is restored.
4. Accept practitioner review if access becomes available; do not manufacture a
   substitute metric while the project remains U0.
