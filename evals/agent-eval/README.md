# Paired agent-eval harness

This directory supports a reproducible same-task comparison between a generic
strategic-risk prompt and the Global Think Tank Analyst runtime method.

It is a **structural sanity check**, not a factual benchmark, external
validation, or evidence of practitioner usefulness. The deterministic scorer
only reports method-contract errors and warnings. It cannot decide whether a
claim is true, supported by a source, or useful to a real decision-maker.

## Suite

`benchmark-cases.jsonl` contains 12 memo tasks across Modes A-G and all four
canonical evidence modes. Case validation enforces a suite size of 10-20 tasks.

## Prepare a run

```bash
python3 scripts/agent_eval.py validate
python3 scripts/agent_eval.py prepare /tmp/gtta-agent-eval --seed 20260830
```

The generated directory contains:

- `requests.jsonl` — 24 shuffled, opaque samples (baseline and skill arm for
  every case);
- `private-mapping.json` — sample-to-arm mapping, case metadata, seed, and the
  exact SHA-256 of `SKILL.md`;
- `outputs.template.jsonl` — the required result shape.
- `antigravity-tasks/` — one provider-neutral Markdown task per opaque sample;
- `antigravity-responses/` — destination for one Markdown response per sample;
- `run-metadata.template.json` — model, app version, and generation settings to
  record before running the tasks.

Send each request's messages to the same model with the same generation
settings. Put each response in the matching `output` field. Do not use the
private mapping to change generation behavior.

## Zero-paid-API Antigravity path

The harness contains no model client and makes no API or network calls. To run
the suite through the locally installed Antigravity application:

1. Fill `run-metadata.template.json` with the visible Antigravity version,
   selected model, and every exposed generation setting.
2. Open each file under `antigravity-tasks/` in a fresh conversation.
3. Save only the final model response as
   `antigravity-responses/<sample_id>.md`.
4. Do not inspect `private-mapping.json` until all 24 responses are saved.
5. Import the responses:

```bash
python3 scripts/agent_eval.py import-antigravity \
  /tmp/gtta-agent-eval \
  /tmp/gtta-agent-eval/antigravity-responses \
  --metadata /tmp/gtta-agent-eval/run-metadata.template.json \
  --output /tmp/gtta-agent-eval/outputs.jsonl
```

Import records hashes of the request and output files in `run-metadata.json`.
It fails on missing, unknown, or empty responses.

## Verify a replication is materially fresh

Before presenting a repeated run as independent evidence, compare its outputs
with every earlier run or discarded attempt that used the same cases:

```bash
python3 scripts/agent_eval.py verify-freshness \
  /tmp/gtta-agent-eval \
  /tmp/gtta-agent-eval/outputs.jsonl \
  --against evals/agent-eval/runs/PRIOR_RUN \
  evals/agent-eval/runs/PRIOR_RUN/outputs.jsonl \
  --report /tmp/gtta-agent-eval/freshness-report.json
```

The gate rejects exact copies and likely cosmetic rewrites. A near-duplicate
is flagged when normalized whole-text similarity is at least 0.90 or when at
least 0.80 of non-empty lines are shared exactly. These disclosed heuristics
can produce false positives or miss sophisticated reuse; passing them does not
prove independent generation. Fresh isolated conversations and an auditable
execution record remain mandatory procedural evidence.

## Score a completed run

```bash
python3 scripts/agent_eval.py score \
  /tmp/gtta-agent-eval \
  /tmp/gtta-agent-eval/outputs.jsonl \
  --report /tmp/gtta-agent-eval/report.json
```

The report compares pass rates and rule-level findings. A same-family or
author-run delta must remain labelled as self-scored structural evidence. It
must not be described as external validation or overall model quality.

Published generation outputs and their original report are immutable. When a
checker heuristic changes, keep the original report and add a separately named
rescore against the frozen outputs. A rescore evaluates checker behavior; it is
not a new model run.

## Published runs

- [`2026-09-01 — Antigravity / Claude Opus 4.6 (Thinking), seed 20260902`](runs/2026-09-01-antigravity-claude-opus-4.6-thinking-seed-20260902/):
  fresh post-runtime-change replication with a passed freshness gate against
  all three earlier runs. The skill arm passed 12/12 versus 0/12 for the
  baseline and stored 111 capped warnings versus 359. Three skill samples hit
  the warning cap; the `1.2.3` rescore also identifies 11 truncated baseline
  samples. The reduction from the prior Claude rescore's 170 is directional
  rather than a precise quality estimate.
- [`2026-08-31 — Antigravity / Claude Opus 4.6 (Thinking), seed 20260901`](runs/2026-08-31-antigravity-claude-opus-4.6-thinking-seed-20260901/):
  cross-model-family execution with a passed freshness gate against both
  Gemini runs. The skill arm passed 12/12 versus 0/12 for the baseline, but
  produced 181 capped warnings versus 360. The `1.2.2` frozen-output rescore
  reports 170 versus 360 after two narrow precision fixes; the current `1.2.3`
  rescore makes explicit that 2 skill and all 12 baseline samples are
  truncated. The warning triage still records substantial per-claim
  provenance omissions. This extends structural M3 evidence; it is not factual
  or practitioner validation.
- [`2026-08-30 — Antigravity / Gemini 3.7 Flash (High), seed 20260831`](runs/2026-08-30-antigravity-gemini-3.7-flash-high-seed-20260831/):
  post-change same-model replication with a passed near-duplicate gate. The
  original report records 12/12 with 13 warnings for the skill arm and 0/12
  with 254 warnings for the baseline; the current `1.2.3` frozen-output rescore
  reports 12 and 253 warnings respectively. This is replication of structural
  conformance, not independent model-family or practitioner validation.
- [`2026-08-30 — Antigravity / Gemini 3.7 Flash (High)`](runs/2026-08-30-antigravity-gemini-3.7-flash-high/):
  12/12 contract passes with the skill vs. 0/12 for the generic baseline. Exact
  requests, outputs, metadata, private mapping, report, hashes, and limitations
  are committed for audit and deterministic rescoring; the current `1.2.3`
  rescore reports 25 skill and 248 baseline warnings.
