# Source and information grading (optional, Admiralty-style)

An optional field for **load-bearing claims that are disputed or rest on a single
source**. It is not required on every claim and no validator enforces it.

## The two scales

Grade the source and the information separately. A reliable source can pass on a
doubtful claim, and a doubtful source can be right.

Source reliability (track record of the source):

| Grade | Meaning |
|---|---|
| A | Reliable: consistent record of accuracy |
| B | Usually reliable |
| C | Fairly reliable |
| D | Not usually reliable |
| E | Unreliable |
| F | Cannot be judged |

Information credibility (this specific claim):

| Grade | Meaning |
|---|---|
| 1 | Confirmed by independent sources |
| 2 | Probably true: consistent with other information |
| 3 | Possibly true: plausible, not confirmed |
| 4 | Doubtful |
| 5 | Improbable |
| 6 | Cannot be judged |

Written as a pair, for example `B2` or `C3`. This is the NATO/Admiralty system
(NATO AJP-2.1 and the US Army FM 2-22.3 tables). Verify the wording against those
documents before citing it in a client deliverable.

## When to use it

Use it only when all of these hold:

- the claim changes the judgment or the recommendation,
- the claim is disputed, single-sourced, or from a state or interested party,
- the reader would otherwise not see why the claim was trusted.

Typical fit: sanctions, trade-route and customs claims where official statements
and press reports disagree.

## How to record it

Add it next to the existing provenance tag, not instead of it:

```
Claim: Transit volume on the route fell in Q3. [secondary] grade: C3
Source note: single trade-press report, no customs data found.
```

Rules:

1. The grade describes the source's track record and the claim's corroboration.
   It is not a confidence label and does not replace Low / Moderate / High.
2. Do not average grades across claims. Show the grade of the claims the
   judgment depends on.
3. Source dependence matters: two outlets repeating one statement is one source.
   Mode G (ACH) already tracks source dependence; use it there.
4. If you cannot justify a grade in one line, write `F6` or leave the field out.
   Do not invent a grade to fill the field.
