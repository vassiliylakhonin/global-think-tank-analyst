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

## Check an existing bundle

The checker requires only the core GTTA package, not Agenda Intelligence:

```bash
gtta check-review-bundle memo.review
gtta check-review-bundle memo.review --json
```

The versioned JSON report uses `gtta.review-bundle-check@1.0`. The checker
requires the exact file set, rejects symbolic links and non-file entries,
validates the manifest and input-digest declarations, recomputes every output
hash, parses the verification receipt and SARIF, and derives `passed` again
from strictness, Agenda validity, packet status, and GTTA findings. It also
checks that the manifest, receipt, and repair status agree.

Stable rule families are:

| Rule | Meaning |
|---|---|
| `GTTAB001` | Missing or unexpected bundle file |
| `GTTAB002` | Symbolic link or non-regular bundle entry |
| `GTTAB003` | Invalid manifest JSON |
| `GTTAB004` | Unsupported bundle interface |
| `GTTAB005` | Invalid manifest invariant |
| `GTTAB006` | Wrong output declaration set |
| `GTTAB007` | Invalid output metadata |
| `GTTAB008` | Output hash mismatch |
| `GTTAB009` | Invalid verification receipt |
| `GTTAB010` | Inconsistent or impossible status |
| `GTTAB011` | Invalid SARIF output |
| `GTTAB012` | Repair-status mismatch |
| `GTTAB013` | Invalid input digest declaration |

The checker exits `0` for an internally valid bundle, including an intact
bundle whose recorded memo verification is `REVIEW REQUIRED`. Its text and
JSON reports expose that verdict separately as `verification_passed` and
`packet_status`. It exits `1` for bundle-contract or integrity findings and `2`
when the requested path does not exist, is not a directory, or cannot be read.

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

The manifest is self-contained but not signed. A matching SHA-256 proves only
that a file matches the value currently declared in that manifest; it does not
prove who produced either file or that an adversary did not replace both. Use
an external signature or trusted artifact attestation when authenticity is
required.
