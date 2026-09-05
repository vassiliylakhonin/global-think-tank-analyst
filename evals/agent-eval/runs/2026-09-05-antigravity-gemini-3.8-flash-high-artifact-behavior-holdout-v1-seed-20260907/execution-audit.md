# Execution audit

This audit was written before publication from the Antigravity execution log
and the retained run artifacts.

## Verified

- The public preregistration commitment predates the generated outputs in Git.
- All committed case, expectation, request, skill, and schema hashes match.
- There are 20 unique expected sample IDs and 20 non-empty JSON objects.
- Every raw response exactly equals its imported `outputs.jsonl` value.
- Both arms contain 10 samples and all report aggregates reconcile to sample
  detail.
- A fresh scorer invocation reproduces `report.json` byte for byte.
- The repository remained clean during Antigravity execution.

## Procedural qualifications

- One initial subagent invocation was stopped and restarted after its delivery
  configuration was edited. No output from the stopped attempt was accepted.
  The metadata's `retry count: 0` therefore understates total orchestration
  attempts by one under the broad meaning of retry.
- The operator derived baseline/skill identity from request contents to define
  separate subagent templates. The final model contexts were isolated, but the
  orchestration process was not arm-blind.
- Several final JSON objects were transferred from transcript records into
  response files through orchestration scripts. File/import equality is
  verified; semantic non-editing is a procedural assertion rather than a
  cryptographically verifiable property.
- Existing runs cannot be used with `verify-freshness` because their case IDs
  differ. No freshness claim is made for this new suite.

These qualifications do not change the deterministic 0/10 versus 0/10 result.
They do limit how strongly the run can support claims about independent or
fully blinded execution.
