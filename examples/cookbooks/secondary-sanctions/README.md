# One-minute cookbook: Central Asia microelectronics routing

This deterministic, offline example demonstrates the complete shipped seam:

```text
MemoArtifact -> GTTA projection -> Agenda Intelligence check -> review bundle
```

The documents and entities are synthetic. Evidence mode is
`illustrative source packet`; this is not a sanctions-screening result, legal
advice, or evidence about a real counterparty.

## Run

From the repository root:

```bash
python -m pip install -e ".[verification]"
python examples/cookbooks/secondary-sanctions/run.py
```

The script validates `memo.json`, auto-discovers `memo.sources.json`, selects
source-backed claims, loads only their declared local sources, runs Agenda
Intelligence's deterministic packet checker in strict mode, and atomically
writes `review-bundle/`. The directory contains the rendered memo, JSON and
Markdown receipts, side-by-side HTML, SARIF, bounded repair guidance, and a
hash-bearing manifest. A passing run says that no deterministic repair is
needed; a failing run still writes the complete bundle and lists safe,
claim-level repair actions without copying the source documents. Open
`review-bundle/review.html` to inspect claims, lexical support, source excerpts,
and reviewer actions side by side.

Review directories are immutable by convention and never overwritten. Move or
archive `review-bundle/` before rerunning this exact cookbook command.

To exercise the fail-closed path, change either dated fact in `memo.json`
without changing its source, or set its `verify` field to `false`, then run the
script again. The script exits non-zero and keeps human review required.

The optional live counterparty worker is intentionally not part of the default
run: network availability and current sanctions data would make this example
non-reproducible. A live adapter should be a separate, explicitly enabled
stage and must never upgrade this packet-completeness result into legal
clearance.

## Regression benchmark

The repository-level benchmark reuses this synthetic packet without changing
it:

```bash
python scripts/run_verification_benchmark.py
```

It checks two golden variants and four controlled failures, emits SARIF 2.1.0,
and verifies that bounded repair guidance never authorizes invented evidence.
