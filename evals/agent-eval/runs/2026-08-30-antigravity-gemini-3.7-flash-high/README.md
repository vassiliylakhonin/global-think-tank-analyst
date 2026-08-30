# Antigravity paired run — 2026-08-30

This is the first completed run of `gtta-agent-eval@1.1.0`. It compares the
same 12 tasks under a generic strategic-risk system prompt and the GTTA runtime
method. Samples were shuffled and identified opaquely before generation.

## Run conditions

| Field | Value |
|---|---|
| Runner | Antigravity 2.11.0 |
| Model | Gemini 3.7 Flash (High) |
| Thinking | `high` |
| Temperature | `1.0` |
| Seed | `20260830` |
| Samples | 24: 12 baseline, 12 skill |
| Benchmark | `gtta-agent-eval@1.1.0` |
| Scorer | `gtta-method-contract@1.1.0` |
| Skill SHA-256 | `acadddecc71444687e85db2aca442a887c6e0606fa08fead1d187923aae167dd` |
| Requests SHA-256 | `4ead20edb05644335f8f3facb75e975d1b6915e2a25b7518fc6ff8d4689fe4c0` |
| Outputs SHA-256 | `16bfd3f04bbaf560bf4de8e1a31c11f03518e060840bb53759d9f9fbda76ac2f` |
| Original scorer source | Git commit `bfb0877` |

The application version was initially entered as `2.0` and corrected during
evidence verification to the `2.11.0` version reported by the installed macOS
application bundle. Generation used the local application; the harness made no
model API or network calls.

## Result

| Arm | Passed | Pass rate | Errors | Warnings |
|---|---:|---:|---:|---:|
| Generic baseline | 0 / 12 | 0% | 36 | 283 |
| GTTA skill | 12 / 12 | 100% | 0 | 72 |

This result supports a narrow claim: under these tasks and settings, attaching
the GTTA method improved compliance with the deterministic GTTA method contract.
It does not establish factual accuracy, source support, decision quality,
general model quality, practitioner usefulness, or production reliability. The
baseline was not instructed in GTTA-specific syntax, so the delta must not be
presented as an independent quality benchmark.

## Frozen-output ruleset rescore

The original `gtta-method-contract@1.1.0` report above is immutable. The same
24 outputs were rescored with `gtta-method-contract@1.2.0`; no model was called
and no output was edited.

| Arm | Passed | Pass rate | Errors | Warnings |
|---|---:|---:|---:|---:|
| Generic baseline | 0 / 12 | 0% | 36 | 249 |
| GTTA skill | 12 / 12 | 100% | 0 | 25 |

The skill-arm reduction from 72 to 25 removes 47 layout false positives: three
semantically equivalent Mode C/E headings and 44 metadata, table-header,
identifier-column, or direct-question findings. The remaining GTTA010 findings
are actionable untagged analytical lead-ins or claim-bearing table cells. This
rescore measures checker precision, not a new improvement in model output.

## Published artifacts

- [`requests.jsonl`](requests.jsonl) — exact shuffled inputs;
- [`private-mapping.json`](private-mapping.json) — arm and case mapping;
- [`outputs.jsonl`](outputs.jsonl) — exact model outputs;
- [`run-metadata.json`](run-metadata.json) — generation settings and hashes;
- [`report.json`](report.json) — aggregate and per-sample deterministic results.
- [`rescore-gtta-method-contract-1.2.0.json`](rescore-gtta-method-contract-1.2.0.json)
  — current-ruleset rescore of the unchanged outputs.

To reproduce the score from the repository root:

```bash
python3 scripts/agent_eval.py score \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high/outputs.jsonl
```

That command uses the current installed ruleset and should match the separately
named rescore. Reproducing the immutable original report requires the source at
git commit `bfb0877`.
