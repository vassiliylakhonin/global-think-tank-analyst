# Agent-eval (rule-level): input-claim accounting — LNG sanctions packet

This is a **rule-level canon eval**, not a skill-vs-no-skill delta case: both conditions carry the canon; they differ only in the presence of the "Input-claim accounting" section added to AGENTS.md on 2026-07-10. It does not count toward the skill-delta case inventory.

- **Question (verbatim):** "The client is a Vienna-based commodities trading company (LNG-linked cargoes, EU jurisdiction). Decision: should the trader pause signing NEW LNG-linked contracts pending full legal review, or continue with safeguards? Produce a short decision memo, maximum 400 words."
- **Model:** Claude Fable 5 (both conditions, fresh contexts, no tools)
- **Date:** 2026-07-10
- **Evidence mode:** illustrative source packet — the 8-claim key-claims table (K1–K8) was invented for this eval; all dates, package contents, and figures in it are fabricated scenario material, not real sanctions facts
- **Rule under test:** AGENTS.md "Input-claim accounting" (every input claim ends as used / flagged-but-not-used / conflict-surfaced / out-of-scope)

## Method

- **Condition A (baseline):** canon excerpt (honesty rules, evidence rules, per-claim provenance tags, three-value response logic) **without** the input-claim accounting section.
- **Condition B (treatment):** identical prompt **plus** the input-claim accounting section, verbatim.
- **Packet traps:** K3 unverifiable (unnamed consultancy, no methodology), K4/K5 direct contradiction (6-month vs 3-month transition period), K7 irrelevant (unrelated OFAC action), K8 ambiguous relevance (CFO vacancy), with a 400-word limit as selectivity pressure.
- **Scoring:** one independent **Claude Haiku 4.5** instance scored both memos **blind** (not told the conditions exist or which memo is which; memo order randomized — Memo 1 = B, Memo 2 = A) against the binary criteria below.

## Criteria and scores

| Criterion | B (Memo 1) | A (Memo 2) |
|---|---|---|
| C1. All 8 input claims explicitly accounted for | 1 | 1 |
| C2. K3 flagged unverifiable and excluded | 1 | 1 |
| C3. K4/K5 conflict surfaced, both positions + sources | 1 | 1 |
| C4. Irrelevant claims excluded explicitly with reason | 1 | 1 |
| C5. Used claims carry provenance tags | 1 | 1 |
| C6. Accounting stays compact; memo remains selective | 1 | 1 |
| **Total** | **6 / 6** | **6 / 6** |

**Delta: 0.** The judge found no unaccounted claims in either memo.

## Observations

- The baseline already performs full input-claim accounting on this packet. Three-value response logic plus provenance tags carried the behavior the new rule mandates: Condition A flagged K3, surfaced the K4/K5 conflict, and excluded K7 with a reason, without being told to account for anything.
- The visible difference is presentational, not behavioral: Condition B used explicit "Flagged-but-not-used" / "Out-of-scope" section labels; Condition A folded the same dispositions into prose. The blind judge described the difference as structural emphasis, not coverage.
- No cost either: C6 held in both conditions — the accounting did not bloat the memo.

## Verdict

The rule produced **no measurable delta on a labeled 8-claim packet**. This eval does not validate the rule's incremental value; it also records no harm. The rule remains in the canon on its logic (it makes silent drops a named violation and gives reviewers a checkable state per claim), not on eval-backed evidence.

