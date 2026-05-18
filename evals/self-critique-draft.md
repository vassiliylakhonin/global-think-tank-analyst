# Self-critique pass for canon-rule failure modes — RESOLVED

**Status (updated 2026-05-18):** Decision gates ran in [`self-runs/2026-05-18-fm-validation.md`](self-runs/2026-05-18-fm-validation.md). Outcome:

- **FM-A (table-cell tag drift) — ADOPTED.** Reproduced 2/2 in fresh context against current canon; proposed critic resolved it 2/2 with no length inflation. Self-check bullet integrated into `SKILL.md` and recorded as item 18 in [`failure-modes.md`](failure-modes.md).
- **FM-B (ceremonial Rule 2 vs Step 5) — NOT ADOPTED.** Did not reproduce 0/2 in fresh context. Current canon already prevents the failure mode; adding a critic would solve a non-problem. If FM-B is observed again with a captured floor-test prompt, re-open this analysis.

This file is retained as a record of the decision-gate process. Sections 1-8 below are the original PROPOSAL text from 2026-05-13/14, preserved for reference and not re-edited.

**Intent (original):** Draft a minimal, opt-in self-critique block to address two reproducibly observed failure modes before deciding whether to integrate into `SKILL.md`.
**Author note (original):** Per project policy, canon (`SKILL.md`, `AGENTS.md`) is not edited based on a draft. Two prior floor-test observations are insufficient for canon integration — see [Decision gates](#decision-gates) below.

---

## 1. Observed failure modes

Two patterns have been informally observed across two floor-tests (not yet reproduced under fresh-context conditions):

### FM-A — Table-cell provenance tag drift

**Symptom:** Axis A tags (`[primary]` / `[secondary]` / `[inference]` / `[analyst-judgment]`) are present in body prose but **drop, mutate, or get reassigned inside markdown table cells** — typically in the Risks/Options/Indicators tables.

**Suspected cause:** Visual compression pressure inside narrow table cells; the model treats tags as decorative and prunes them under perceived layout constraints.

### FM-B — Ceremonial application of "Flag-but-don't-use" (Three-value Rule 2) where Workflow Step 5 was the correct frame

**Symptom:** Where the memo should give a primary judgment with a competing interpretation (Workflow Step 5: "Generate competing interpretations"), it instead applies the Three-value Rule 2 ("Flag-but-don't-use") to *every* alternative interpretation, ending up with no committed primary view.

**Suspected cause:** Conflation of two distinct discipline rules:
- *Three-value Rule 2* — meant for uncertain factual claims that should not load-bear analysis.
- *Workflow Step 5* — meant for ambiguous interpretive frames where the analyst should commit to a primary view while showing a meaningful alternative.

The agent applies the more cautious of the two when in doubt, which reads as ceremonial hedging.

---

## 2. Hypothesis

A short, named self-critique pass — run silently before final output — that explicitly tests for these two patterns will reduce their recurrence without lengthening the memo or weakening current discipline.

This is the "generator → critic → revise" pattern (commonly called *self-refine* in the NLP literature). It is widely used; it is not guaranteed to work on every model; it must be validated on this skill's actual outputs.

---

## 3. Proposed addition to `SKILL.md`

**Insertion point:** at the end of the existing "Self-check before finalizing" block (currently SKILL.md lines 472–490), as two additional silent-check items. No existing item is removed or rewritten.

**Proposed text (English, to match `SKILL.md`):**

```markdown
- For each table that includes claims (Risks, Options, Indicators, Actors): does every factual cell carry an Axis A tag, matching the tag the same claim would carry in body prose? If any cell drops or mutates a tag under layout pressure, restore it.
- For each ambiguous interpretive frame in the memo: did I commit to a primary judgment with a named competing interpretation (Workflow Step 5), rather than apply "Flag-but-don't-use" (Three-value Rule 2) to every alternative? Rule 2 is for uncertain factual claims that should not load-bear analysis; Step 5 is for committing to a primary interpretive view while showing the strongest alternative. If I have shown only alternatives without a primary view, choose the better-supported primary view and reframe alternatives as Step 5 competing interpretations.
```

**Why two bullets and not a separate section:** the existing self-check is the established home for silent verification. Adding new structure (sub-headers, separate critic pass) would expand surface area without evidence the structure is load-bearing.

---

## 4. Test scaffolding

The two floor-tests that produced these observations are not stored in the repo. To validate this draft, the following before/after structure should be filled in with **the actual prompts and outputs** from those tests:

### Test 1 — Table-cell tag drift

- **Prompt used (from floor-test):** _[paste prompt]_
- **Output without critic (observed FM-A):** _[paste excerpt showing dropped/mutated tags in table]_
- **Output with critic (to be generated):** _[run same prompt with the proposed self-check addition]_
- **Pass criterion:** every factual cell in every table carries an Axis A tag consistent with body prose.

### Test 2 — Ceremonial Rule 2

- **Prompt used (from floor-test):** _[paste prompt]_
- **Output without critic (observed FM-B):** _[paste excerpt showing all-alternatives-no-primary-view pattern]_
- **Output with critic (to be generated):** _[run same prompt with the proposed self-check addition]_
- **Pass criterion:** memo commits to a primary interpretive judgment and frames alternatives as Step 5 competing interpretations; "Flag-but-don't-use" appears only for genuinely uncertain factual claims, not for interpretive frames.

### Optional: negative test

Run the critic on a memo that did **not** exhibit either FM. Pass criterion: no spurious rewrites, no tone change, no length inflation beyond ~5%.

---

## 5. Success metric

Integration into `SKILL.md` is justified only if **all** of the following hold:

1. Both Test 1 and Test 2 pass on the *original* floor-test prompts.
2. At least **two additional fresh-context reproductions** of FM-A and FM-B are produced without the critic, and the critic resolves them. (This satisfies the "need fresh-context observations before canon edits" rule.)
3. The negative test shows no regression on a clean memo.
4. Memo length does not grow by more than ~5% on average across the four tests.

If any of these fails, document which and do **not** integrate.

---

## 6. Risks

- **Token cost.** A self-check pass adds latency and cost. Two bullets is minimal; if integration succeeds, watch for scope creep into a heavyweight critic.
- **Over-correction.** The critic might rewrite analytically-correct hedging as false commitment. The negative test guards against this but only weakly with a single example.
- **Model-specific behavior.** What works on one model may not transfer. Re-test on at least one alternative model before treating as model-agnostic.
- **Hidden coupling.** Adding self-check items may interact with the existing self-check block in unforeseen ways. Read the final list end-to-end after insertion to check for redundancy or contradiction.

---

## 7. Decision gates

Before any edit to `SKILL.md`:

1. The two original floor-test prompts/outputs must be located and pasted into the Test scaffolding above. Without them, the validation is not anchored.
2. Two fresh-context reproductions of each FM must be collected.
3. The critic text above must be reviewed for tone consistency with the rest of `SKILL.md` (terse, imperative, no hedging in the meta-instructions).

If gates 1–3 pass, propose a single small commit: insert the two bullets at the end of the self-check block; no other change. Update `evals/failure-modes.md` to add FM-A and FM-B as items 18 and 19 with their diagnostic cues and the critic as the fix. Move this draft file's status from PROPOSAL to ADOPTED, or delete it if the failure-modes.md addition supersedes it.

---

## 8. What this draft does not do

- Does not modify `AGENTS.md`, `SKILL.md`, or `evals/failure-modes.md`.
- Does not claim the proposed critic works. Until validated, it is hypothesis.
- Does not name a specific paper or technique. "Self-refine" is referenced as a class of pattern, not a citation.
- Does not introduce any new evaluation infrastructure, scoring, or schema.
