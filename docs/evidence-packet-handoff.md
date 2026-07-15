# Evidence-packet handoff

Global Think Tank Analyst produces the reasoning and memo. [Agenda Intelligence MD](https://github.com/vassiliylakhonin/agenda-intelligence-md) is primarily a deterministic evidence-packet linter for claim-backed AI output.

The handoff seam is a small JSON packet:

1. Draft the memo with Global Think Tank Analyst.
2. Select externally checkable factual and quantitative claims. Do not turn scenarios, assumptions, `[inference]`, or `[analyst-judgment]` statements into sourced facts.
3. Give every selected claim a stable `claim_id` and declare the `source_ids` it relies on.
4. Copy caller-supplied source text into `sources[]`. A URL or citation alone is not source text.
5. Add `quotes[]` only for verbatim spans that appear in the named source.
6. Run the packet through Agenda Intelligence MD before human review.

If a factual claim has no supplied support, keep the claim in the packet with an empty `source_ids` array. Do not invent a source to make the packet pass. The linter should report that gap.

## Runnable synthetic example

The example is intentionally synthetic and contains no real policy claim:

```bash
pip install "agenda-intelligence-md==1.3.0"
agenda-intelligence check examples/evidence-packet-handoff.json --strict
```

Example: [`examples/evidence-packet-handoff.json`](../examples/evidence-packet-handoff.json).

## Interface limits

The linter checks references, declared quotes, lexical support, and unmatched numbers. It reports packet completeness, not factual truth, source authority, legal sufficiency, or whether the memo's judgment is sound. Human review remains required.

Decision record: [`docs/adr/0001-use-evidence-packet-handoff-as-primary-agenda-seam.md`](adr/0001-use-evidence-packet-handoff-as-primary-agenda-seam.md).
