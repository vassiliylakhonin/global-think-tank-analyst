# Verification-flag development cases

Ten new development cases isolate unsupported externally checkable premises and
include two hypothetical controls. These are **development data**, not a fresh
holdout, benchmark result or evidence of improved behavior. Existing holdouts,
expectations and model outputs remain unchanged. `min_verify_claims: 0` on controls
is not a maximum; inspect spurious flags separately in human review.

## Full versus compact comparison

Prepare paired baseline/full and baseline/compact runs with identical questions,
output contracts, model, tool access (none), budgets and settings. Use separate
fresh contexts and at least three independent repetitions. Preserve generated
responses, provider logs, token usage, truncation and retry history. Commit each
preparation before running it; do not edit cases or thresholds after seeing results.

```bash
python scripts/agent_eval.py prepare-artifact-behavior /tmp/gtta-full-dev \
  --cases evals/skill-improvement/verification-development/cases.jsonl \
  --expectations evals/skill-improvement/verification-development/expectations.json \
  --suite-version gtta-verification-development@1 --seed 20260930
python scripts/agent_eval.py prepare-artifact-behavior /tmp/gtta-compact-dev \
  --cases evals/skill-improvement/verification-development/cases.jsonl \
  --expectations evals/skill-improvement/verification-development/expectations.json \
  --skill evals/skill-improvement/compact-candidate.md \
  --suite-version gtta-verification-development@1 --seed 20260930
```

Score with the existing `score-artifact-behavior` command after generation and
response import. The shared seed yields aligned case/arm IDs for comparison;
keep the two output directories separate. Reports assess declared structure and
behavior, not whether content is true or decisions are good. Qualitative review
must cover reasoning loss, unsupported premises used downstream, and unnecessary
stops; a shorter prompt is not adopted solely for better flag counts.

The compact candidate is opt-in and unvalidated. Freeze a **new** unseen holdout
only after development is finished. No model run accompanies this change.
