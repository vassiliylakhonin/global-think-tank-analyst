# Project status

Updated 2026-08-30. Maturity definitions are in
[`docs/maturity-framework.md`](docs/maturity-framework.md); gates for specific
claims are in [`docs/definition-of-done.md`](docs/definition-of-done.md).

## Current coordinates: R2 / M2 / U0

| Axis | Level | Evidence | Next level requires |
|---|---:|---|---|
| Release readiness | R2 | GitHub pre-release `v1.5.0rc1`; source, distribution, and installed-wheel gates; Trusted Publishing workflow on `main` | Restore PyPI account access, register the pending publisher, publish through the protected workflow, and verify installation from PyPI |
| Method evidence | M2 | Versioned Markdown contract, strict `gtta.memo@1.0` artifact with per-claim provenance, regression tests, and a declared 12-case paired harness | Execute and publish the controlled paired run with a bounded predeclared structural claim and full settings |
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
- The repository has predeclared evaluation cases but no completed aggregate
  paired-run result.
- External practitioner usefulness and production reliability are unvalidated.

## Immediate development order

1. Keep `gtta.memo@1.x` and `gtta-method-contract@1.x` stable and testable.
2. Execute the paired 12-case structural evaluation when model access and a
   reproducible run budget are available.
3. Complete PyPI Trusted Publishing after account access is restored.
4. Accept practitioner review if access becomes available; do not manufacture a
   substitute metric while the project remains U0.
