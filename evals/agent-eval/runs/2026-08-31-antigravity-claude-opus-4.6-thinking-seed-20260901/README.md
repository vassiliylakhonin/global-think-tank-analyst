# Antigravity cross-model paired run — seed 20260901

This is a cross-model-family execution of `gtta-agent-eval@1.1.0`. It compares
the same 12 tasks under a generic strategic-risk system prompt and the GTTA
runtime method. Samples were shuffled and identified opaquely before
generation.

## Run conditions

| Field | Value |
|---|---|
| Runner | Antigravity 2.11.0 |
| Model | Claude Opus 4.6 (Thinking) |
| Recorded generation settings | None exposed or recorded (`{}`) |
| Seed | `20260901` |
| Samples | 24: 12 baseline, 12 skill |
| Benchmark | `gtta-agent-eval@1.1.0` |
| Scorer | `gtta-method-contract@1.2.1` |
| Skill SHA-256 | `0184f9f8b3283d33d31b00e2928b98629f1e746e4b9d9cbd6bfcbc70db28f334` |
| Requests SHA-256 | `ba4e27edd4c586a73acf27fd6dae663d93027ecdf42a955c87f985190a96050f` |
| Outputs SHA-256 | `5f5c22f59548e2105b3833e72b6f30222c48c2fcadb381be8ad9884665dd6a52` |

Generation used the locally installed application and its built-in model
selection; the harness made no model API or network calls. The application
version was initially entered as `2.0`. Before publication it was corrected to
`2.11.0` after checking the installed macOS application bundle. The correction
is disclosed in `run-metadata.json`; no generated response was changed.

## Result

| Arm | Passed | Pass rate | Errors | Warnings |
|---|---:|---:|---:|---:|
| Generic baseline | 0 / 12 | 0% | 30 | 360 |
| GTTA skill | 12 / 12 | 100% | 0 | 181 |

The result repeats the bounded pass-rate delta on a second model family: under
these tasks, prompts, and deterministic checks, attaching the GTTA method
improved compliance with the GTTA method contract. The generic baseline was
not instructed in GTTA-specific syntax.

The warning result is equally important. The skill arm produced 181 warnings,
far more than either Gemini run under the same current ruleset. This shows that
the binary pass gate is coarse and that per-claim provenance instructions did
not transfer cleanly to this Claude execution. Two samples reached the
scorer's 25-warning cap, so 181 is the reported capped count, not a complete
census of all possible Markdown findings.

The committed [warning triage](warning-triage-gtta-method-contract-1.2.1.md)
separates confirmed checker noise from likely method-conformance omissions.
It records 12 false positives on the mandatory evidence-access disclosure, one
false positive on a quoted rejection of generic advice, two valid missing
Mode C trigger markers, and a large mixed set of provenance warnings. The
frozen outputs and original report are not edited to improve the result.

This run does not score factuality, source support, decision quality, overall
model quality, or practitioner usefulness. It remains author-operated
structural evidence. It strengthens M3 but does not change external-usefulness
status U0.

## Freshness check

The committed `freshness-report.json` compares this run with both published
Gemini runs by case and arm. It found no exact or threshold near-duplicates.
Across both comparisons, maximum normalized whole-text similarity was
`0.246765` against a `0.90` threshold and maximum shared-line ratio was
`0.192308` against a `0.80` threshold.

These heuristics can identify likely reuse or superficial rewriting but cannot
prove independent generation. Fresh isolated contexts and the execution record
remain procedural evidence, not a mathematical guarantee.

## Published artifacts

- [`requests.jsonl`](requests.jsonl) — exact shuffled inputs;
- [`private-mapping.json`](private-mapping.json) — arm and case mapping;
- [`outputs.jsonl`](outputs.jsonl) — exact final model outputs;
- [`run-metadata.json`](run-metadata.json) — runner, model, hashes, and the
  disclosed application-version correction;
- [`report.json`](report.json) — aggregate and per-sample deterministic result;
- [`warning-triage-gtta-method-contract-1.2.1.md`](warning-triage-gtta-method-contract-1.2.1.md)
  — bounded human disposition of the skill warnings;
- [`freshness-report.json`](freshness-report.json) — reproducible comparisons
  with both earlier published runs.

To reproduce the score and freshness comparison from the repository root:

```bash
python3 scripts/agent_eval.py score \
  evals/agent-eval/runs/2026-08-31-antigravity-claude-opus-4.6-thinking-seed-20260901 \
  evals/agent-eval/runs/2026-08-31-antigravity-claude-opus-4.6-thinking-seed-20260901/outputs.jsonl

python3 scripts/agent_eval.py verify-freshness \
  evals/agent-eval/runs/2026-08-31-antigravity-claude-opus-4.6-thinking-seed-20260901 \
  evals/agent-eval/runs/2026-08-31-antigravity-claude-opus-4.6-thinking-seed-20260901/outputs.jsonl \
  --against \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high/outputs.jsonl \
  --against \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high-seed-20260831 \
  evals/agent-eval/runs/2026-08-30-antigravity-gemini-3.7-flash-high-seed-20260831/outputs.jsonl
```
