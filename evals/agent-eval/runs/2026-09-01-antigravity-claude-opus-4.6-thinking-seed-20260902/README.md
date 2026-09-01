# Antigravity Claude post-change replication — seed 20260902

This is a fresh same-model-family replication of `gtta-agent-eval@1.1.0`
after the GTTA runtime instructions were tightened for canonical Axis A tags
and explicit Mode C trigger headings. It compares the same 12 tasks under a
generic strategic-risk prompt and the updated GTTA skill.

## Run conditions

| Field | Value |
|---|---|
| Runner | Antigravity 2.11.0 |
| Model | Claude Opus 4.6 (Thinking) |
| Recorded generation settings | None (`{}`) |
| Seed | `20260902` |
| Samples | 24: 12 baseline, 12 skill |
| Benchmark | `gtta-agent-eval@1.1.0` |
| Scorer | `gtta-method-contract@1.2.2` |
| Skill SHA-256 | `fbf1f2c2957c0fa7701aabbc4484de954726311ee9c7f74f3b8979837117d57a` |
| Requests SHA-256 | `8fac5bb130cf32e2741de652566397268ea095c5c70ada12e7db3232e9890ed8` |
| Outputs SHA-256 | `fad6a6d60988dbab7bc24e06d37ec86edfa7e40d672fcfbaeef52a65233f00d1` |

The execution conditions were carried from the prefilled template and the
operator reported no deviation. Generation used the Antigravity built-in model
selection and no external API key. The local harness only imported, hashed,
scored, and compared the saved outputs; it made no model call.

## Result

| Arm | Passed | Pass rate | Errors | Warnings |
|---|---:|---:|---:|---:|
| Generic baseline | 0 / 12 | 0% | 32 | 359 |
| GTTA skill | 12 / 12 | 100% | 0 | 111 |

The result repeats the bounded contract-pass delta on fresh Claude outputs.
Compared with the previous Claude run rescored under the same `1.2.2` ruleset,
the stored skill warning count falls from 170 to 111. That difference is
consistent with better runtime-instruction transfer, but it is not a causal
estimate: the seed and generated outputs also changed.

Three skill samples reached GTTA010's 25-finding cap, versus two in the prior
Claude rescore. Therefore 111 is a capped stored count, not a complete census,
and the apparent 59-warning reduction must not be presented as a precise
quality improvement. The [warning triage](warning-triage.md) records 73
table-cell and 37 prose GTTA010 findings, one Mode C marker omission, and the
per-case cap boundary. No warning used `[assumption]`, `[unknown]`, or
`[scenario]` as a substitute for Axis A, which is encouraging but still only
one run.

This benchmark does not score factuality, source adequacy, decision quality,
overall model quality, or practitioner usefulness. Maturity remains
`R2 / M3 / U0`.

## Frozen-output ruleset 1.2.3 rescore

The original `gtta-method-contract@1.2.2` report remains immutable. Ruleset
1.2.3 stores the same findings and adds explicit cap telemetry: 11 baseline
samples and 3 skill samples are truncated for GTTA010. The 359 and 111 warning
counts are therefore lower bounds for those arms, not complete totals.

## Freshness check

The committed `freshness-report.json` compares this run with both Gemini runs
and the prior Claude run. It found no exact or threshold near-duplicates.

| Reference | Max sequence similarity | Max shared-line ratio |
|---|---:|---:|
| Gemini seed 20260830 | 0.242900 | 0.192308 |
| Gemini seed 20260831 | 0.223549 | 0.192308 |
| Claude seed 20260901 | 0.410396 | 0.355556 |

The thresholds are 0.90 and 0.80. Passing this heuristic reduces detected
reuse risk but cannot prove independent generation.

## Published artifacts

- [`requests.jsonl`](requests.jsonl) — exact shuffled inputs;
- [`private-mapping.json`](private-mapping.json) — arm and case mapping;
- [`outputs.jsonl`](outputs.jsonl) — exact final model outputs;
- [`run-metadata.json`](run-metadata.json) — declared execution record and
  hashes;
- [`report.json`](report.json) — deterministic aggregate and per-sample score;
- [`rescore-gtta-method-contract-1.2.3.json`](rescore-gtta-method-contract-1.2.3.json)
  — current-ruleset rescore with explicit truncation telemetry;
- [`warning-triage.md`](warning-triage.md) — bounded disposition of skill
  warnings;
- [`freshness-report.json`](freshness-report.json) — reproducible comparisons
  against all three earlier runs.

To reproduce the score from the repository root:

```bash
python3 scripts/agent_eval.py score \
  evals/agent-eval/runs/2026-09-01-antigravity-claude-opus-4.6-thinking-seed-20260902 \
  evals/agent-eval/runs/2026-09-01-antigravity-claude-opus-4.6-thinking-seed-20260902/outputs.jsonl
```
