# Validation Plan

This plan describes how to move the strategic-risk agent portfolio from
"early but credible public artifacts" toward externally reviewed usefulness.

It is not evidence that validation has happened. It is the operating plan for
collecting that evidence without inflating claims.

## Goal

Produce a small number of reviewable case packets that a domain practitioner can
evaluate for usefulness, evidence discipline, and decision relevance.

The target outcome is not "accuracy" or a benchmark score. The target outcome is
practitioner feedback on whether the workflow is useful, where it fails, and
what revisions would make it more operationally credible.

## What Counts As Validation

Validation requires an identifiable external reviewer or practitioner. A valid
review record should include:

- reviewer role or relevant expertise;
- case packet reviewed;
- date of review;
- whether the reviewer found it useful, useful with revisions, or not useful;
- specific findings and requested changes;
- whether findings were incorporated, rejected, or deferred;
- attribution preference: public name, role-only, anonymized, or private record.

Self-review by the author does not count as external validation.

## What Does Not Count

- More polished README language.
- More examples written by the author.
- A self-assigned scorecard.
- CI passing.
- LLM praise or informal model feedback.
- Stars, forks, downloads, or page views.
- Claims such as "trusted by", "production-grade", "validated", or "used by"
  without attributable evidence.

## Candidate Case Packets

Start with three case packets. Each should be small enough for a reviewer to
read in 20-30 minutes.

| Case | Primary repo | Vertical depth | Validation layer | Reviewer target |
|---|---|---|---|---|
| Central Asia fintech routing risk | Global Think Tank Analyst | Central Asia + Caspian skill | Agenda Intelligence MD | sanctions / AML / fintech risk |
| Gulf correspondent-banking exposure | Global Think Tank Analyst | Gulf + Middle East skill | Agenda Intelligence MD | banking compliance / correspondent banking |
| EU industrial tariff / regulatory exposure | Global Think Tank Analyst | optional vertical context | Agenda Intelligence MD | trade policy / industrial strategy |

## Required Packet Structure

Each packet should include:

1. User prompt and decision context.
2. Evidence mode and source boundary.
3. Memo produced using Global Think Tank Analyst.
4. Any vertical-specialist augmentation used.
5. Agenda Intelligence MD validation/scoring output, if used.
6. Final decision brief.
7. Known limitations.
8. Reviewer questions.
9. Review record placeholder.

## Minimum Review Questions

Ask every reviewer:

- Is the decision question clear?
- Are facts, assumptions, assessments, scenarios, and unknowns separated well?
- Are the evidence limits honest?
- Are the role-based implications useful?
- Are the watch-next indicators concrete enough?
- What would make this unsafe or misleading in your workflow?
- What one revision would most improve usefulness?
- Would this be useful, useful with revisions, or not useful?

## Recording Findings

Create a review record only after a real reviewer response exists. Store it in a
future `validated-cases/` or `reviews/` directory only if the reviewer consents
to the chosen attribution level.

If permission is not granted, summarize privately but do not publish identifying
details.

## Current Status

No external validation is claimed by this plan. It prepares the workflow for
external review.

