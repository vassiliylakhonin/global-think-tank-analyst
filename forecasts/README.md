# Forecast log

A plain record of dated, resolvable judgments, so hit rates can be counted later.

**Status: started 2026-11-09.** Six forecasts logged from real memos, none
resolved yet; no calibration is claimed. Entries must be real judgments from real
memos. Do not add invented ones. Synthetic examples live only in
`tests/test_forecasts.py` and are marked synthetic there.

Format and terms: [`docs/estimative-language.md`](../docs/estimative-language.md).

## What counts as a loggable forecast

- A claim about a future event or state, with a specific resolution date.
- A resolution rule written before the date, checkable from a named public source.
- A probability in 1-99 percent (use the term bands in the language table).
- Optional: the indicator the forecast was drawn from, and the memo it came from.

Vague claims ("tension will rise") are not loggable. Rewrite them or leave them out.

## `log.csv` columns

| Column | Meaning |
|---|---|
| id | Stable id, e.g. `f-0001` |
| logged_on | Date logged (YYYY-MM-DD) |
| claim | One resolvable sentence |
| probability | Integer percent that the claim resolves YES |
| resolve_by | Date the question closes (YYYY-MM-DD) |
| resolution_rule | What counts as YES, and the source to check |
| memo_ref | Memo or case it came from (optional) |
| indicator | Related indicator (optional) |
| outcome | Empty until resolved, then `yes` or `no` (or `void` if the question became unresolvable) |
| resolved_on | Date resolved |
| notes | Optional |

Never edit `claim`, `probability` or `resolve_by` after logging. If you change your
mind, add a new row. Editing the past destroys the record.

## Scoring ritual

Run it when entries pass `resolve_by`, at least once a quarter:

1. Resolve due entries from the named source. Fill `outcome` and `resolved_on`.
   Mark `void` rather than guessing.
2. Run `python forecasts/score.py`. It prints counts, Brier score, and a hit
   table by probability band, and flags entries past `resolve_by` that are unresolved.
3. Compare with the **base rate**: the Brier score of always forecasting the
   observed share of YES outcomes. A score is only interesting if it beats that.
4. Do not read calibration from fewer than about 30 resolved entries. The script
   prints a warning below that. Below it, treat results as anecdotes.
5. Write what you learned (where you were over- or underconfident) in a short note,
   and adjust future probabilities, not past rows.

Brier score: mean of (probability - outcome)^2 with probability as a fraction and
outcome 1 or 0. 0 is perfect; always saying 50% scores 0.25.
