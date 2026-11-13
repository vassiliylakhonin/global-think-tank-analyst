# Evidence age (manual TTL)

`gtta evidence-age memo.json --as-of 2026-11-13` reads a valid
`gtta.memo@2.0` artifact and reports every fact's declared age/expiry, plus
blocks that depend on expired facts. The assessment date is required so runs
are reproducible and do not silently use a machine's timezone.

Optional per-claim fields are `evidence_as_of: "YYYY-MM-DD"` and
`valid_for_days: 10`. Supply both or neither. TTL must be an integer from
1 to 36500, not a boolean. Invalid/overflow calendar dates are rejected.

A fact dated November 1 with TTL 10 expires on November 11: it is within TTL
on November 10 and expired at the start of November 11. Dates are calendar days,
not elapsed-hour measurements. Future-dated facts are flagged separately.
Missing fields mean `unknown`, never fresh. Non-fact claims do not receive a TTL
assessment, but descendants linked by `basis_claim_ids` are reported as affected
when an ancestor fact expires. The output names claim IDs and declared block
paths (`bottom_line`, `sections.*`, `options.*`, `indicators.*`). It does not infer
links from arbitrary prose or parse free-form Markdown paragraphs.

The canonical v2 renderer displays the declared evidence date and TTL in the
claim ledger. V1 schemas and historical evaluation receipts remain unchanged.

Despite the informal name "half-life", this is an expiry calculator, not
exponential confidence decay. The caller chooses dates and TTLs; there is no
automatic policy for source categories. Within a declared TTL does not mean a
fact is true, supported, unchanged, safe to use, or authoritative. There is no
source retrieval, daemon, notification, automatic rewriting or action.
