# Antigravity paired replication — seed 20260831

This is a same-model post-change replication of `gtta-agent-eval@1.1.0`. It
compares the same 12 tasks under a generic strategic-risk system prompt and the
updated GTTA runtime method. Samples were shuffled and identified opaquely
before generation.

## Run conditions

| Field | Value |
|---|---|
| Runner | Antigravity 2.11.0 |
| Model | Gemini 3.7 Flash (High) |
| Thinking | `high` |
| Temperature | `1.0` |
| Seed | `20260831` |
| Samples | 24: 12 baseline, 12 skill |
| Benchmark | `gtta-agent-eval@1.1.0` |
| Scorer | `gtta-method-contract@1.2.0` |
| Skill SHA-256 | `be463a98f16700c492162f2b334f66ba650940dc39e9976811b5d5d204b01da2` |
| Requests SHA-256 | `8cd3d5bed547809bba9dbf9ae3c1953933a5ada4d4596d51402ec0122a45abe5` |
| Outputs SHA-256 | `51b6d828a8ca7b1be9158a34e22f1d573ce47bb3285015d50764cde8d6e321ea` |

Generation used the local application; the harness made no model API or
network calls. A first candidate reused prior output bytes and was discarded.
A later candidate passed the exact-match check but failed the stricter
near-duplicate gate on six skill samples. Those six samples were regenerated
in isolated contexts; the other 18 already-passing samples were retained. The
final 24-output set is the run published here.

## Result

| Arm | Passed | Pass rate | Errors | Warnings |
|---|---:|---:|---:|---:|
| Generic baseline | 0 / 12 | 0% | 36 | 254 |
| GTTA skill | 12 / 12 | 100% | 0 | 13 |

The 13 skill-arm warnings comprise one GTTA008 output-marker warning and 12
GTTA010 provenance warnings. Compared with the first run's frozen-output
`1.2.0` rescore, skill warnings declined from 25 to 13 while baseline warnings
increased from 249 to 254. This single same-model run cannot isolate whether
the skill-warning change came from the updated runtime instructions, sampling
variation, or both.

The repeated 12/12 versus 0/12 result supports only a bounded claim: under
these tasks and settings, attaching the GTTA method improved compliance with
the deterministic GTTA method contract. The baseline was not instructed in
GTTA-specific syntax. This is not a factual, decision-quality, overall-model,
practitioner-usefulness, or production-reliability benchmark.

## Frozen-output ruleset 1.2.1 rescore

The original `gtta-method-contract@1.2.0` report above is immutable. Rescoring
the same outputs with `gtta-method-contract@1.2.1` removes the missed Mode G
alias from both arms; no model output was edited.

| Arm | Passed | Pass rate | Errors | Warnings |
|---|---:|---:|---:|---:|
| Generic baseline | 0 / 12 | 0% | 36 | 253 |
| GTTA skill | 12 / 12 | 100% | 0 | 12 |

The 12 remaining skill findings are GTTA010 warnings: ten untagged analytical
recommendation lead-ins and two untagged red-team premise cells. They are
treated as actionable provenance omissions, not checker noise.

## Frozen-output ruleset 1.2.2 rescore

The two narrow 1.2.2 precision refinements do not affect this run. The current
rescore remains 12 skill warnings and 253 baseline warnings, with unchanged
passes and errors.

## Freshness check

The committed `freshness-report.json` compares the final outputs with the first
published run by case and arm. It found no exact or threshold near-duplicates.
The maximum normalized whole-text similarity was `0.854970` against a `0.90`
threshold; the maximum shared-line ratio was `0.583333` against a `0.80`
threshold.

The final bundle also passed the same local gate against the discarded exact-
reuse attempt. Those discarded artifacts are not published as evidence. The
heuristics reduce reuse risk but cannot prove independent generation; the
reported isolated-context procedure remains part of the evidence boundary.

## Published artifacts

- [`requests.jsonl`](requests.jsonl) — exact shuffled inputs;
- [`private-mapping.json`](private-mapping.json) — arm and case mapping;
- [`outputs.jsonl`](outputs.jsonl) — exact final model outputs;
- [`run-metadata.json`](run-metadata.json) — generation settings and hashes;
- [`report.json`](report.json) — aggregate and per-sample deterministic result;
- [`rescore-gtta-method-contract-1.2.1.json`](rescore-gtta-method-contract-1.2.1.json)
  — ruleset-1.2.1 rescore of the frozen outputs;
- [`rescore-gtta-method-contract-1.2.2.json`](rescore-gtta-method-contract-1.2.2.json)
  — current-ruleset rescore of the frozen outputs;
- [`warning-triage-gtta-method-contract-1.2.1.md`](warning-triage-gtta-method-contract-1.2.1.md)
  — disposition of all 12 remaining skill warnings;
- [`freshness-report.json`](freshness-report.json) — reproducible comparison
  with the first published run.

To reproduce the score and published freshness comparison from the repository
root:

```bash
python3 scripts/agent_eval.py score \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high-seed-20260831 \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high-seed-20260831/outputs.jsonl

python3 scripts/agent_eval.py verify-freshness \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high-seed-20260831 \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high-seed-20260831/outputs.jsonl \
  --against \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high/outputs.jsonl
```

The score command uses the current installed ruleset and should match
`rescore-gtta-method-contract-1.2.2.json`, not the immutable original report.
