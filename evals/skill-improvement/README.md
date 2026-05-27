# Skill Improvement Evals

This folder is a lightweight SkillOpt-style loop for improving the runtime skill contract without adding prompt-optimization infrastructure.

It is separate from the existing eval layers:

- `evals/rubric.md` scores finished memos with a starter human-review rubric.
- `evals/adversarial/` contains stress cases for trust-layer behavior.
- `evals/agent-eval/` records with/without structural deltas when the skill is used in agent workflows.
- `evals/skill-improvement/` evaluates proposed edits to `SKILL.md` and `codex/SKILL.md` before accepting them.

This is not a factual benchmark, model-quality comparison, practitioner review, or validation claim. It is a change-control surface for the skill instructions.

## Files

- `cases/global-think-tank-analyst.jsonl` - validation cases for the runtime skill contract.
- `rubric.md` - manual scoring rubric for skill responses.
- `runs/global-think-tank-baseline.md` - baseline against the current skill contract.
- `tools/validate_cases.py` - local JSONL case validator.

## Workflow

1. Add or update cases before changing skill instructions.
2. Score the current skill against `val` cases.
3. Make the smallest useful edit to `SKILL.md` and any runtime copy that must stay aligned.
4. Re-score the same `val` cases.
5. Accept the edit only if validation improves and no boundary regresses.

## Acceptance Rule

Accept a skill edit only when all are true:

- Average `val` score improves by at least `0.5` on the 10-point rubric, or a critical boundary failure is fixed.
- No `val` case drops by more than `1.0`.
- The edit preserves the repo boundary: no legal/compliance/investment advice, no factual verification claim, no live retrieval claim unless retrieval actually happened.
- The edit stays short enough that the skill remains usable.

## Validate Cases

```bash
python3 evals/skill-improvement/tools/validate_cases.py \
  evals/skill-improvement/cases/global-think-tank-analyst.jsonl
```
