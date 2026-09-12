# Project status

Updated 2026-09-12. Maturity definitions are in
[`docs/maturity-framework.md`](docs/maturity-framework.md); gates for specific
claims are in [`docs/definition-of-done.md`](docs/definition-of-done.md).

## Current coordinates: R3 / M3 / U0

| Axis | Level | Evidence | Next level requires |
|---|---:|---|---|
| Release readiness | R3 | `1.6.0` is on PyPI (uploaded 2026-09-07T12:02:04Z, sdist + wheel) through an authenticated workflow running this repository's full release gate, and installs from there into a clean environment: `pip install global-think-tank-analyst==1.6.0`, then `import gtta`, `gtta artifact-schema`, and the 45/45 Russian method including Mode G. **Caveat, and it is the point of the R axis:** that workflow ran in a sibling repository, because this one still cannot authenticate to PyPI. R3 is the highest defined release level | — |
| Method evidence | M3 | Four disclosed Markdown runs report 12/12 skill passes vs. 0/12 baseline. Declared-behavior runs on the original suite record 8/12 vs. 3/12 on Gemini and 3/12 vs. 0/12 on Claude. The preregistered broader-domain holdout passed structure 10/10 in both arms but declared behavior 0/10 in both; the null result and execution caveats are retained. | M3 is the highest defined method level; stronger quality/usefulness claims require different evidence and remain tracked under U |
| External usefulness | U0 | No external practitioner review record exists; `reviews/` contains scaffolding only | One real review reaches U1; two independent relevant reviews with recorded findings reach U2 |

## Release state

- Latest stable release: [`v1.6.0`](https://github.com/vassiliylakhonin/global-think-tank-analyst/releases/tag/v1.6.0), superseding the `rc1`-`rc3` candidates.
- Package version on `main`: `1.7.0rc1`, the unreleased candidate containing the Agenda Intelligence verification bridge and SARIF support.
- `v1.6.0rc1` is superseded: its release build failed before packaging because
  the workflow omitted the optional LangChain test dependency. `rc2` passed
  the corrected distribution-integrity gate; its PyPI job was intentionally
  skipped.
- **The PyPI blocker was narrower than recorded.** It was stated as "account
  recovery / two-factor access", and account access is indeed impaired:
  `pypi/support#12033` has been open since 2026-08-28. But an API token does
  not need a second factor to upload — a web login does, and a web login is
  what registering a Trusted Publisher requires. The sibling repository
  `agenda-intelligence-md` published six releases on a stored token over the
  same period, most recently `1.8.0` on 2026-08-28. This repository was blocked
  because it offered only the credential that needs the login.
- That token is account-scoped, not project-scoped: it was created at
  `2026-05-01T17:44:48Z`, five minutes before that project's first upload at
  `17:49:52Z`, and a project-scoped token cannot exist before its project does.
- **`1.6.0` was published from that sibling repository on 2026-09-07**, through a
  dispatch-only bridge workflow that checked this repository out at the tag,
  refused to run against any other project name, and repeated this repository's
  own release gate before uploading. The bridge has since been deleted; the
  commit that removed it names the revert if it is needed again.
- **This repository still cannot publish itself.** Its own `publish-pypi.yml`
  accepts a stored token or Trusted Publishing and has neither: no secret is set
  here, and no publisher is registered. Two runs of it on `v1.6.0` built cleanly
  and failed at upload. Making the next release self-sufficient needs either a
  registered Trusted Publisher (owner `vassiliylakhonin`, repository
  `global-think-tank-analyst`, workflow `publish-pypi.yml`, environment `pypi`)
  or this repository's own copy of a token.
- No prerelease is sent to PyPI automatically.

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
- The Claude Code / Opus 4.6 replication passed 3/12 skill samples versus 0/12
  baseline on declared behavior, while structural passes were 11/12 versus
  12/12. It repeats the direction across a second model family but not the
  magnitude, and the low absolute pass rate prevents a strong adoption claim.
- The preregistered 10-case broader-domain holdout passed strict structure in
  both arms but passed zero complete declared-behavior expectations in either
  arm. Missing `verify: true` declarations dominated. This does not reproduce
  the original suite's positive combined-pass difference and limits any claim
  of reliable cross-domain contract transfer.
- External practitioner usefulness and production reliability are unvalidated.

## Immediate development order

1. Keep `gtta.memo@1.x` and `gtta-method-contract@1.x` stable and testable.
2. Keep the new per-sample truncation telemetry in every published rescore and
   avoid presenting capped warning totals as exact quality deltas.
3. Freeze the completed holdout and its null result; do not tune the skill or
   thresholds against these 10 cases.
4. Complete PyPI Trusted Publishing after account access is restored.
5. Accept practitioner review if access becomes available; do not manufacture a
   substitute metric while the project remains U0.
