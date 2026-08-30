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

- [`2026-08-30 — Antigravity / Gemini 3.7 Flash (High)`](runs/2026-08-30-antigravity-gemini-3.7-flash-high/):
  12/12 contract passes with the skill vs. 0/12 for the generic baseline. Exact
  requests, outputs, metadata, private mapping, report, hashes, and limitations
  are committed for audit and deterministic rescoring.
