# Case Packet Reviewer Workflow

Use this workflow when asking a domain practitioner to review a public case
packet.

This is not external validation by itself. It is the review path that helps a
reviewer give useful criticism without implying production use, compliance
approval, or benchmark status.

## Review Goal

Ask whether the packet is useful as a decision-support starting point, where it
is too generic, where it overreaches, and what evidence would be required before
operational use.

Do not ask the reviewer to endorse the project, score it as a benchmark, or
approve real-world use.

## Materials To Send

Send the reviewer these files:

- [case-packet.md](case-packet.md) - human-readable source-backed case packet.
- [case-packet.brief.json](case-packet.brief.json) - machine-readable decision
  logic, scenarios, watchlist, evidence mode, and confidence.
- [case-packet.evidence.json](case-packet.evidence.json) - source mapping,
  support status, source limits, unsupported claims, and missing sources.
- [external-review-template.md](external-review-template.md) - response form.

Optional context:

- [VALIDATION_PLAN.md](../VALIDATION_PLAN.md) - what counts as validation.
- [evals/checklist.md](../evals/checklist.md) - general memo quality checklist.
- [evals/rubric.md](../evals/rubric.md) - optional qualitative scorecard.

## Review Sequence

1. Read the top limitation note in `case-packet.md`.
2. Read the user prompt and decision snapshot.
3. Read the source base and source limitations.
4. Check the claim traceability matrix.
5. Skim the source-backed memo for decision usefulness.
6. Compare the markdown packet against `case-packet.brief.json`.
7. Compare key claims against `case-packet.evidence.json`.
8. Fill in `external-review-template.md`.

## Reviewer Should Check

- Whether the decision question is realistic for fintech risk or compliance
  leadership.
- Whether facts, assumptions, assessments, scenarios, and unknowns are separated.
- Whether the source base is adequate for a public demo.
- Whether any claim is too strong for the evidence mode.
- Whether the unsupported and missing-source lists are honest.
- Whether the recommended posture follows from the evidence and assumptions.
- Whether the watch-next indicators are observable enough.
- Whether the packet could mislead a non-expert into treating it as operational
  advice.

## Output Expected From Reviewer

Minimum useful response:

- verdict: useful as a starting point, useful with revisions, not useful, or
  outside review scope;
- three strongest findings;
- required revisions before the packet could be operationally credible;
- sources or evidence that would be mandatory before use;
- attribution preference: public name, role-only, anonymized, or private.

## Maintainer Response

After receiving feedback:

1. Do not publish the review unless permission is explicit.
2. Separate findings into incorporated, rejected, and deferred.
3. Record only the attribution level the reviewer allowed.
4. Do not claim external validation unless a real review exists.
5. Update the packet, JSON projection, and validation plan if findings change
   the case boundary or evidence claims.

## Current Status

No external reviewer has reviewed the current case packet.

