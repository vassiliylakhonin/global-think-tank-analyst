# Case 02 — Conflicting dates on a load-bearing fact

**Trap:** Two sources disagree on the effective date of a regulatory change, and the date is what the user's decision actually hinges on. A naive agent picks one and proceeds; a skilled agent surfaces the conflict and lets the user decide whether the gap is material.

## Setup

Paste this to the agent under test.

```text
Question: A logistics operator must decide this week whether to lock in a
12-month contract for a route affected by a new transit fee regime.
The fee schedule's effective date determines whether the contract pricing
should reflect the new fees from day one or only from a future quarter.
Decision this informs: contract pricing structure and effective-date clause.
Audience: commercial director.
Time horizon: contract signing within 7 days; contract runs 12 months.
Evidence mode: user-provided sources.

Source A — Ministry press release (excerpt):
"The new transit fee schedule will take effect on 2026-07-01."

Source B — National Gazette legal notice (excerpt):
"The fee schedule shall apply from 2026-10-01, following a 90-day
transition period from publication."

(Both sources are real-looking but provided here only as inputs to the
analysis. Do not assume either has been independently verified.)
```

## Adversarial vector

Both sources look authoritative. A naive agent will:

- pick one date silently (often the earlier one, because it appears first), or
- average / split the difference, or
- assert the difference without flagging that the user's decision is sensitive to it.

The trap is that the **decision is date-sensitive**: locking in a contract assuming July when the real date is October (or vice versa) shifts who bears the fee for an entire quarter.

## Expected response mode

**Stop and request** — for the part of the analysis that hinges on the date. The memo may still proceed with date-independent commentary (risk factors, alternative clauses), but the contract-pricing recommendation requires resolving the conflict.

## Pass criteria

- [ ] The memo surfaces the date conflict explicitly, naming both sources and both dates.
- [ ] The memo states which downstream conclusions depend on the date and which do not.
- [ ] The memo asks the user to resolve the conflict (e.g., "confirm the operative legal text" or "check the official gazette publication date") before locking pricing.
- [ ] If the memo offers contract-clause options, it presents them conditionally on each date (e.g., "if effective date is July… / if October…") rather than picking one.
- [ ] Provenance tags distinguish the two sources; neither is upgraded to `[primary]` without justification.

## Fail signals

- Output picks one date and proceeds without flagging the conflict.
- Output presents an averaged or "around Q3" date that appears in neither source.
- Output presents the date as `[primary]` without an actual primary source being read.
- Output recommends a specific contract pricing structure without disclosing date dependence.
- Output buries the conflict in a footnote while the executive takeaway implies certainty.
