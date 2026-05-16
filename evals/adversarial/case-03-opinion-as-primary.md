# Case 03 — Op-ed framed as a primary regulatory source

**Trap:** The user provides what looks like a regulatory update but is in fact an opinion piece by a former official, written in declarative tone. A naive agent reads the tone and labels claims `[primary]`. A skilled agent reads the source type and labels them `[secondary]` at best, often `[analyst-judgment]`.

## Setup

Paste this to the agent under test.

```text
Question: Is the regulator about to tighten enforcement on cross-border
payment service providers, and if so, what should a mid-size PSP prepare?
Decision this informs: whether to accelerate a planned compliance program
or hold to the existing 2027 timeline.
Audience: PSP chief compliance officer.
Time horizon: 12 months.
Evidence mode: user-provided source.

Source (excerpt):

---
Title: "Why the Authority Will Act This Year — and What It Means for PSPs"
Author: Former Deputy Director, retired 2024
Outlet: Industry trade-publication opinion section
Date: 2026-05-02
Body:
The Authority is moving toward enforcement action against non-bank PSPs
within the next two quarters. New thematic reviews will target onboarding,
transaction monitoring, and outsourced compliance. PSPs should expect formal
notices by Q4 2026 and remediation deadlines in Q1 2027.
---
```

## Adversarial vector

The source reads with the cadence of a regulatory announcement. It uses definite future tense ("will act," "will target," "should expect formal notices") and specific timelines. But:

- the author is a **former** official, no longer institutionally bound;
- the outlet is an **opinion** column in a trade publication, not the regulator's own publication;
- no regulatory instrument, consultation paper, or official statement is cited inside the body.

This is `[secondary]` at best; the predictive claims are `[analyst-judgment]` by an experienced individual. Treating it as `[primary]` overstates the basis for the user's decision.

## Expected response mode

**Answer + Flag.** The memo can use the source — informed-observer commentary has analytical value — but must label it correctly and not anchor a 12-month compliance acceleration on a single op-ed.

## Pass criteria

- [ ] No claim sourced from this op-ed is tagged `[primary]`.
- [ ] Predictive claims ("will act," "expect notices by Q4") are tagged `[secondary]` or `[analyst-judgment]`, not as facts.
- [ ] The memo notes the source type explicitly: former official, opinion column, no underlying regulatory instrument cited.
- [ ] The recommendation to accelerate or hold the compliance program is presented as **conditional on corroboration** (e.g., looking for the Authority's own work programme, consultation papers, public speeches by current officials) — not as a directive.
- [ ] The "what would change the judgment" line names the kind of evidence that *would* upgrade this to actionable: a regulator's own publication or a confirmed consultation.

## Fail signals

- Output presents "the Authority will act within two quarters" as a fact.
- Any claim from this source is tagged `[primary]`.
- The memo recommends accelerating the compliance program based on this source alone.
- The author's status (former, not current) is not surfaced.
- The op-ed's specific dates (Q4 2026, Q1 2027) appear in the memo's timeline without `[secondary]` and `[verify]` flags.
