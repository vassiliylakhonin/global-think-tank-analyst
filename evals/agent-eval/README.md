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

Send each request's messages to the same model with the same generation
settings. Put each response in the matching `output` field. Do not use the
private mapping to change generation behavior.

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
