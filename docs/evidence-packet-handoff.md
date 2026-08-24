# Evidence-packet handoff

Global Think Tank Analyst produces the reasoning and memo. [Agenda Intelligence MD](https://github.com/vassiliylakhonin/agenda-intelligence-md) is primarily a deterministic evidence-packet linter for claim-backed AI output.

The handoff seam keeps claims explicit and gives Agenda Intelligence MD the
source material in one of two forms:

1. Draft the memo with Global Think Tank Analyst.
2. Select externally checkable factual and quantitative claims. Do not turn scenarios, assumptions, `[inference]`, or `[analyst-judgment]` statements into sourced facts.
3. Give every selected claim a stable `claim_id` and declare the `source_ids` it relies on.
4. Choose the input path:
   - for local source files, create a review manifest whose `sources[]` entries point to paths relative to the manifest;
   - for the inline JSON packet, copy caller-supplied source text into `sources[]`. A URL or citation alone is not source text.
5. Add `quotes[]` only for verbatim spans that appear in the named source.
6. Run the packet through Agenda Intelligence MD before human review.

If a factual claim has no supplied support, keep the claim in the packet with an empty `source_ids` array. Do not invent a source to make the packet pass. The linter should report that gap.

## Install the pinned release

```bash
pip install "agenda-intelligence-md==1.6.0"
```

For PDF input through the local-file workflow, install the optional document
support instead:

```bash
pip install "agenda-intelligence-md[documents]==1.6.0"
```

## Inline JSON packet

The example is intentionally synthetic and contains no real policy claim:

```bash
agenda-intelligence check examples/evidence-packet-handoff.json --strict
```

Example: [`examples/evidence-packet-handoff.json`](../examples/evidence-packet-handoff.json).

## Local-file review

Agenda Intelligence MD 1.6.0 can load caller-selected UTF-8 text, Markdown,
DOCX, and optional PDF files without copying their full contents into JSON.
Claims remain explicit; each source entry supplies a `source_id` and a local
`path` relative to the manifest:

```bash
agenda-intelligence review /path/to/manifest.json --out review.md --strict
agenda-intelligence review /path/to/manifest.json --format json
```

The command runs locally, makes no model or network call, and does not repeat
source text in its result. It does not extract claims from free prose. See the
versioned [local evidence review contract](https://github.com/vassiliylakhonin/agenda-intelligence-md/blob/v1.6.0/docs/evidence-review.md)
and [manifest example](https://github.com/vassiliylakhonin/agenda-intelligence-md/blob/v1.6.0/examples/evidence-review/manifest.json).

The local-file adapter is not exposed by Agenda Intelligence MD's Cloudflare
Workers deployment because a Worker cannot read caller-local file paths. Use
the inline evidence-packet contract for remote integrations.

## Interface limits

Both input paths run the same deterministic linter. It checks references,
declared quotes, lexical support, polarity mismatches, and unmatched numbers.
It reports packet completeness, not factual truth, source authority, legal
sufficiency, or whether the memo's judgment is sound. Human review remains
required.

Decision record: [`docs/adr/0001-use-evidence-packet-handoff-as-primary-agenda-seam.md`](adr/0001-use-evidence-packet-handoff-as-primary-agenda-seam.md).
