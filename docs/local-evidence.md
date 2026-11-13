# Local capture and strict method declarations

These are deterministic preflight tools, not factual verification. No LLM, daemon,
watcher, automatic source discovery, or source-authority rating is involved.

## Capture one explicit URL

```bash
gtta harvest https://example.org/report --out captures --source-id SRC-01
```

This writes `sources.json`, content-addressed `.raw` bytes and UTF-8 `.txt`,
SHA-256 hashes of both, requested/final URLs, content type and UTC retrieval time.
Use a new source ID for each capture. A duplicate ID is refused, not refreshed.
Only public HTTPS port 443 text/plain or HTML is supported. Each redirect is
revalidated; connections pin a checked public IP with TLS hostname verification.
No ambient cookies, credentials or proxy environment are used. Private/reserved
addresses, non-200 responses, excessive redirects, compressed bodies, captures
over 2 MB, and unsupported encodings/types fail closed. There is a 15-second
socket timeout and a 45-second capture deadline checked between reads/hops;
platform DNS resolution itself is not deadline-bounded.

HTML extraction is deliberately small: no JavaScript, browser rendering, PDF,
OCR, paywall bypass or hidden-text detector. Text is whitespace-normalized per
line, with script/style content omitted. The raw bytes remain available. Captured
text is untrusted data, not instructions. It is never executed or sent to an LLM.

Hashes detect accidental or partial changes, not forgery by someone who can
rewrite both the manifest and snapshots. This is not a signature or independent
proof of when a page existed. Save files in an operator-owned directory; this is
not a hostile-filesystem sandbox or a concurrent multiwriter store.

## Strict Markdown profile

```bash
gtta check-contract memo.md --mode B --strict --json
gtta check-contract memo.md --mode B --sources captures/sources.json --json
```

`--strict` selects `gtta-method-contract@2.0.0`. Existing calls retain v1 rules,
severities, schema hashes and exit behavior. `--sources` implies strict and does
only local reads, never network retrieval.

- GTTA011: a populated `Null hypothesis: ...` no-action baseline, outside Mode F.
- GTTA012: every **declared source-backed fragment** (`[primary]`, `[secondary]`,
  `[user-provided]`) needs an inline `[SRC-XX]`, at least two digits. Table cells
  are checked separately. This is declaration checking, not semantic discovery
  of every factual sentence. Untagged claims still receive the v1 heuristic
  warning. Exact `kind: fact` accounting belongs to the JSON artifact ledger.
- GTTA013: deeper modes B/E/G need a `gtta-reversals` block. If declared in any
  mode, it must be a nonempty JSON list with valid typed fields.
- GTTA014: a `gtta-quotes` block must be a valid nonempty JSON list; quotes must
  occur as exact, case-sensitive contiguous substrings of the captured text.
- GTTA015: with `--sources`, all cited IDs must exist, both file hashes must match,
  and extracted text must be reproducible from the saved raw bytes. Declared
  quotes without a manifest fail because literal checking is unavailable.

```text
[primary] The pilot has a capped budget. [SRC-01]
[analyst-judgment] Prefer a reversible pilot.
Null hypothesis: If no action is taken, retain the existing operating posture.
```

An example declaration (synthetic values, not a forecast or recommendation):

```gtta-reversals
[{"metric":"pilot loss","operator":">=","threshold":10.0,"unit":"USD","review_by":"2026-12-01","action":"Pause the pilot."}]
```

```gtta-quotes
[{"source_id":"SRC-01","quote":"a capped budget"}]
```

Reversal checks validate fields, finite numeric thresholds, operators and real
calendar dates. They do not measure the metric, monitor dates, evaluate whether
the threshold was crossed, or trigger actions. Null-hypothesis checking establishes
only a populated declaration, not the quality or plausibility of that baseline.
Quote presence does not establish that the quote supports the claim, that the
source is authoritative, or that the source is current. Ordinary quotation marks
are not machine quote declarations.

## Structured artifact

`gtta artifact-schema --strict` exposes the separate `gtta.memo@2.0` schema.
It adds `null_hypothesis` and `reversal_conditions`; v2 validation requires the
baseline outside F, reversals in B/E/G, and SRC-XX IDs for every `kind: fact`.
The canonical renderer preserves these fields and emits inline references.
`gtta check-artifact memo.json --strict` enforces those requirements even on a v1
input, which normally needs migration. No v1 schemas, archived prompts or
published evaluation receipts have been rewritten. V2 has no new analytical
quality benchmark claim.

MCP `check_memo_contract`, `check_memo_artifact` and `get_memo_artifact_schema`
accept `strict=True`. Capture and reading arbitrary local snapshot paths are CLI
operations only; they are not added as remotely callable MCP filesystem/network
tools.

## Agenda compatibility

The optional verification dependency is constrained to `>=1.9.0,<1.25`.
The canonical golden and negative-control integration tests pass with 1.9.0 and
1.24.0. They fail with 1.25.0 even on the unchanged earlier GTTA tree, so support
for that version is not claimed. The evidence-packet algorithm and fixtures are
unchanged; do not weaken checks or reinterpret a failed golden case as success.
