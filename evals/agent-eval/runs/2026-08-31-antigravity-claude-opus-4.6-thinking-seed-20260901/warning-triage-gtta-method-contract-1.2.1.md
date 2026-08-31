# Warning triage — Claude run, ruleset 1.2.1

This review covers the 181 skill-arm warnings in the immutable
`gtta-method-contract@1.2.1` report. It does not edit generated responses or
assess whether their substantive claims are true.

## Count boundary

`GTTA010` stops after 25 likely untagged claims per sample. The
`conflicting-policy-dates` and `infrastructure-attribution` skill samples both
reached that cap. Therefore 178 is the exact number of GTTA010 findings stored
in this report, but not necessarily the total number the heuristic could have
emitted without its output cap. Warning comparisons must use this limitation.

## Disposition

| Finding set | Count | Disposition |
|---|---:|---|
| GTTA010 on the exact mandatory `EVIDENCE ACCESS LIMITED` disclosure | 12 | Confirmed checker noise: the scope disclosure is not an analytical claim |
| GTTA009 on `monitor the situation` | 1 | Confirmed checker noise: the output quotes the phrase while explicitly replacing it with if-then logic |
| GTTA008 missing Mode C `triggers` marker | 2 | Actionable: the CBAM and Hormuz memos contain scenarios but no explicit trigger section or accepted alias |
| Other GTTA010 findings stored in the report | 166 | Mixed, predominantly actionable provenance coverage gaps; see categories below |

Of all 178 GTTA010 findings, 92 point to individual non-label table cells and
86 to prose lines. The table-cell count is not duplicate noise by itself: the
contract requires provenance for each claim-bearing cell, even when another
cell in the same row is tagged.

## Recurring actionable patterns

- Non-canonical labels such as `[assumption]` and
  `[unknown — decision-relevant]` are not Axis A provenance tags.
- User-supplied statements are repeated without `[user-provided]` on the
  specific claim.
- A tag in one table cell is treated as if it covers adjacent claim-bearing
  cells; it does not under the method contract.
- Analytical lead-ins, recommendations, scenario premises, and implications
  appear without `[inference]` or `[analyst-judgment]`.
- The two Mode C outputs named above omit the required trigger shape even
  though they include baseline and scenario sections.

The heuristic can still over-flag layout prose or under-detect claims. Exact
claim accounting requires `MemoArtifact`; this triage should not be read as a
claim that all 166 remaining findings were individually adjudicated.

## Confirmed checker-follow-up candidates

Two narrow changes are justified for a future ruleset, after preserving this
original report:

1. Exempt the exact required limited-evidence disclosure from GTTA010.
2. Avoid GTTA009 when a generic-advice phrase is quoted as an anti-pattern and
   the same sentence explicitly supplies observable if-then logic.

Neither change should suppress the valid Mode C trigger findings or relax
per-cell provenance coverage.
