# Validation Plan

This plan owns the external-usefulness (`U`) axis: how to move from no recorded
practitioner evidence toward externally reviewed usefulness. Release readiness
and method evidence are tracked separately in [`STATUS.md`](STATUS.md).

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
5. Agenda Intelligence MD evidence-packet review output, if used.
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

For the current Central Asia fintech routing-risk packet, use
[`docs/headless-workflow.md`](docs/headless-workflow.md) to send the packet,
machine-readable projections, and response template in a consistent order.

## Recording Findings

Create a review record only after a real reviewer response exists. Store it in
[`reviews/`](reviews/) only if the reviewer consents to the chosen attribution
level. Use [`reviews/TEMPLATE.md`](reviews/TEMPLATE.md) for the record.

If permission is not granted, summarize privately but do not publish identifying
details.

## Current Status

Updated 2026-08-30.

- **External practitioner review:** none recorded. The [`reviews/`](reviews/)
  directory contains only `TEMPLATE.md` and `README.md`. No reviewer record
  exists yet. The plan prepares the workflow for external review; it does not
  claim that review has happened.
- **Current usefulness coordinate:** U0. This does not block software releases
  or method experiments; it blocks practitioner-usefulness and production-use
  claims. See [`docs/definition-of-done.md`](docs/definition-of-done.md).
- **Agent-eval delta cases:** three cases are committed under
  [`evals/agent-eval/`](evals/agent-eval/): CBAM enforcement, Baltic cable
  attribution, and input-claim accounting for an LNG sanctions packet. The
  CBAM case is a self-scored structural delta. The Baltic case uses two blind
  judges, including one cross-vendor judge, and reports a judge-dependent
  delta of +2 to +4. The input-claim-accounting case uses one same-vendor blind
  judge and reports a delta of 0. These are structural checks, not factual,
  practitioner, or production validation.
- **Paired structural harness:** 12 memo tasks across Modes A-E and G are declared in
  [`evals/agent-eval/benchmark-cases.jsonl`](evals/agent-eval/benchmark-cases.jsonl).
  `scripts/agent_eval.py` prepares same-model baseline/skill requests and can
  score either deterministic Markdown method-contract findings or strict
  `MemoArtifact` structure. Four Markdown runs are published with their exact
  artifacts and limitations. The first structured run is also published: its
  baseline passed 10/12 and skill arm 1/12 because protocol 1.0.0 omitted exact
  machine-key guidance. Protocol 1.1.0 corrects that adapter but has not yet
  been executed. Neither path measures factual or decision quality.
- **Skill change-control cases:**
  [`evals/skill-improvement/`](evals/skill-improvement/) contains 10 declared
  cases: 6 `val`, 2 `train`, and 2 `test`. The six validation cases were
  manually rescored from 52/60 to 58/60 after a runtime-contract sync. The two
  test cases are labelled as holdouts but have not been executed as a release
  gate. The case validator checks JSONL structure only. These results are not
  a benchmark or an external validation claim.
- **Sibling repository scores are not evidence for this repo:** portfolio
  comparisons must name each repository's native framework. See
  [`docs/maturity-framework.md`](docs/maturity-framework.md).
- **No production usage, no adoption numbers, no benchmark scores** are
  claimed by this repo or by the vertical specialists.
