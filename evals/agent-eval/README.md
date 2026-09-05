# Paired agent-eval harness

This directory supports a reproducible same-task comparison between a generic
strategic-risk prompt and the Global Think Tank Analyst runtime method.

It is a **structural sanity check**, not a factual benchmark, external
validation, or evidence of practitioner usefulness. The deterministic scorer
only reports method-contract errors and warnings. It cannot decide whether a
claim is true, supported by a source, or useful to a real decision-maker.

## Suite

`benchmark-cases.jsonl` contains 12 memo tasks across Modes A-E and G and three
canonical evidence modes: reasoning-only, user-provided sources, and an
illustrative source packet. It contains no Mode F coaching task and no
live-source-backed task. Case validation enforces a suite size of 10-20 tasks;
those coverage gaps belong in a future versioned suite, not a rewrite of this
frozen benchmark.

New suites are preregistered under [`commitments/`](commitments/). The first
holdout commitment covers 10 broader-domain cases, including the previously
absent Mode F. Its cases and hidden expectations are intentionally withheld
until the first 20 paired outputs have been saved; the committed hashes bind
their exact pre-run contents.

The same frozen cases can now be run through the strict
[`MemoArtifact` path](artifact-eval.md). Both arms receive the same schema and
output contract; only the skill arm receives the runtime method. This avoids a
trivial format-knowledge advantage while measuring exact declared claim-ledger
conformance separately from Markdown heuristics.

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

For structured JSON output, use `prepare-artifact`, the same
`import-antigravity` command, and `score-artifact`. Its pass condition is valid
`gtta.memo@1.0` structure plus exact expected Mode and evidence-mode matching.
See the [structured protocol](artifact-eval.md) for commands and limitations.
The versioned `prepare-artifact-behavior` / `score-artifact-behavior` path adds
preregistered case-specific declaration minima after structural validation. It
is intended to break the schema ceiling while remaining explicitly narrower
than semantic or practitioner evaluation.

## Published structured runs

- [`2026-09-05 — Claude Code / Claude Opus 4.6, declared-behavior replication`](runs/2026-09-05-claude-code-opus-4.6-thinking-artifact-behavior-seed-20260906/):
  the skill arm passed 3/12 frozen behavior expectations versus 0/12 baseline;
  structural passes were 11/12 versus 12/12. This repeats the positive
  direction across a second model family but not the Gemini magnitude. The low
  absolute adoption and one source-reference failure remain visible.
- [`2026-09-04 — Antigravity / Gemini 3.7 Flash (High), declared-behavior protocol 1.0.0`](runs/2026-09-04-antigravity-gemini-3.7-flash-high-artifact-behavior-v1-seed-20260905/):
  both arms passed 12/12 structural checks. The skill arm passed 8/12 frozen
  declared-behavior expectations versus 3/12 for baseline. Freshness passed
  against both earlier structured runs. The observed `+41.7` point difference
  is a one-run method-contract result, not a semantic-quality or usefulness
  score.
- [`2026-09-04 — Antigravity / Gemini 3.7 Flash (High), artifact protocol 1.1.0`](runs/2026-09-04-antigravity-gemini-3.7-flash-high-artifact-v1.1-seed-20260904/):
  fresh post-correction run with 12/12 passes and no findings in both arms.
  Freshness passed against 1.0.0. This confirms the narrow adapter repair but
  provides no positive skill delta because schema conformance reached a ceiling.
- [`2026-09-02 — Antigravity / Gemini 3.7 Flash (High), artifact seed 20260903`](runs/2026-09-02-antigravity-gemini-3.7-flash-high-artifact-seed-20260903/):
  the first strict `MemoArtifact` run. Baseline passed 10/12 and skill 1/12.
  The published failure triage traces 10 skill failures to unmapped
  human-readable section headings and one to a `ClaimKind`/provenance
  collision. Protocol 1.1.0 corrects the shared output instructions; the fresh
  post-change run above confirms that narrow correction.

## Published Markdown runs

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
