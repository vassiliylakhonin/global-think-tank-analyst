# Two-case portfolio cookbook

This developer-facing cookbook runs two real, source-backed `MemoArtifact`
examples through the shipped GTTA → Agenda Intelligence seam:

- Kazakhstan critical-raw-materials investment framing;
- Middle Corridor sanctions-risk decision gates.

Both examples declare `live-source-backed` evidence mode. They are dated
snapshots, not current legal, sanctions, compliance, or investment advice.
Re-check every source and claim before operational use.

## Run

From the repository root:

```bash
python -m pip install -e ".[verification]"
python examples/cookbooks/flagship-portfolio/run.py
```

The command builds both cases in an isolated staging directory, requires
`PASS / packet_complete`, verifies the review-bundle file and hash contract,
and then atomically promotes the complete release directory. A failed build
leaves the previous release unchanged.

The default output is `artifacts/flagship-portfolio/` and contains:

- one seven-file review bundle per case;
- one deterministic downloadable ZIP per case;
- `summary.json` with case counts, source counts, bundle hashes, and explicit
  limitations.

Each review bundle includes the rendered memo, JSON and Markdown receipts,
side-by-side HTML, SARIF 2.1.0, bounded repair guidance, and a SHA-256 manifest.
Passing establishes deterministic structural and lexical completeness—not
factual truth, source authority, legal sufficiency, or decision safety. Human
review remains required.

The cookbook is exercised by the repository's Agenda 1.9 integration job.
Its generated release files are CI artifacts rather than committed outputs.
