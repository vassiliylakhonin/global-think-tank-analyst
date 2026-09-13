# Review bundle

`gtta review` turns one validated, source-backed `MemoArtifact` into a fixed,
auditable directory of human- and machine-readable review outputs. It is the
high-level interface over the existing GTTA-to-Agenda verification seam:

```text
MemoArtifact + source catalog
  -> GTTA validation and projection
  -> Agenda Intelligence packet check
  -> complete review bundle
```

Install the optional verification dependency and run the command from a source
checkout:

```bash
python -m pip install -e ".[verification]"
gtta review memo.json
```

The command auto-discovers `memo.sources.json` beside `memo.json` and writes a
new `memo.review/` directory. Paths can be explicit:

```bash
gtta review memo.json --sources inputs/sources.json --out-dir results/review-001
```

Strict checking is on by default. `--no-strict` is available for diagnostic
work, but it weakens the pass condition and is recorded in the manifest.

## Fixed output contract

Every published `gtta.review-bundle@1.0` directory contains exactly these
files:

| File | Purpose |
|---|---|
| `memo.md` | Human-readable rendering of the validated memo artifact |
| `verification.json` | Deterministic GTTA and Agenda verification receipt |
| `verification.md` | Markdown evidence review |
| `review.html` | Side-by-side browser review |
| `verification.sarif` | SARIF 2.1.0 findings for code-review tooling |
| `repair.md` | Bounded claim-level repair status or instructions |
| `manifest.json` | Interface version, mode, status, limitations, and SHA-256 hashes |

The manifest records both interface versions plus the artifact identity, memo
mode, evidence mode, strictness, and result. It hashes the artifact and source
catalog contents, the text loaded for each used source, and every generated
output other than the manifest itself. It records `human_review_required: true`
even when deterministic checks pass.

## Publication and exit behavior

- The bundle is rendered in a staging directory and renamed into place only
  after every output succeeds.
- An existing output directory is never overwritten. Choose another
  `--out-dir` or deliberately archive the old result first.
- A valid input with evidence gaps still produces the complete bundle and exits
  `1`; this preserves the review evidence needed to repair the memo.
- A complete strict packet exits `0`.
- Invalid inputs, unreadable files, or a missing verification dependency exit
  `2` and do not publish a partial bundle.

`PASS` means the projected packet met the selected deterministic checks. It
does not establish that a claim is true, current, lawful, or safe to act on.
Qualified human review remains mandatory for sanctions, legal, compliance,
financial, and other consequential decisions.
