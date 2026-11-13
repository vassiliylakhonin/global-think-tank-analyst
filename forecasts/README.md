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

## Installed CLI

The original read-only scorer is now packaged; `python forecasts/score.py` remains
compatible. No existing forecast or outcome was changed by this addition.

```bash
gtta forecast-score forecasts/log.csv --as-of 2026-11-13
gtta forecast-add new-forecast.json --ledger my-log.csv
gtta forecast-resolve f-0001 --ledger my-log.csv --outcome yes --resolved-on 2026-12-01 --source 'Named public source and resolution basis'
```

The add command requires a JSON object with `id`, `logged_on`, `claim`, integer
`probability` (1-99), `resolve_by`, and `resolution_rule`. Optional fields match the
CSV columns above. New rows must be unresolved. Duplicate IDs cannot overwrite
old forecasts. Resolution requires a manually supplied yes/no/void, date and basis.
Already resolved outcomes cannot be rewritten with this command. Use operator-owned
files; lock directories and atomic replacement prevent ordinary concurrent writers,
not deliberate filesystem tampering. A crashed writer can leave a `.lock` directory;
check that no writer is active before removing it.

The CLI never retrieves the named source or judges an outcome. Void and pending
entries are excluded from Brier; overdue unresolved IDs are reported. Empty or
unresolved-only ledgers have no Brier score, not a zero score. At least 30 resolved
entries is only a cautionary minimum, not proof of calibration or predictive skill.
The report always disclaims a calibration claim. Existing six entries remain
pending; synthetic forecasts are only test fixtures.
