# Live demo: composing this skill with Agenda Intelligence MD

This doc walks through an actual end-to-end run with real CLI output. It uses the [`live-source-backed-memo`](../../examples/live-source-backed-memo.md) example and its [JSON projection](../../examples/agenda-projections/live-source-backed-memo.brief.json) and [evidence pack](../../examples/agenda-projections/live-source-backed-memo.evidence.json).

The numbers below are real outputs from `agenda-intelligence` (PyPI package version installed on 2026-05-08). They are not sample placeholders.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install agenda-intelligence-md
agenda-intelligence --version
```

## Step 1 — Validate the JSON projection

```bash
agenda-intelligence validate-brief examples/agenda-projections/live-source-backed-memo.brief.json
```

Output (real):

```text
OK: agenda brief validates
```

## Step 2 — Score the structured brief (no evidence pack)

```bash
agenda-intelligence score examples/agenda-projections/live-source-backed-memo.brief.json
```

Output (real):

```text
score: 95/100
note: Heuristic structural/evidence-discipline score; does not verify factual truthfulness.
relevance: 25/25 - clear topic, change, and affected actors
evidence_support: 21/25 - evidence_mode=live_source_backed; no evidence pack provided; confidence level provided
completeness: 20/20 - all required fields present; optional fields present: 5/5
actionability: 14/15 - watch-next indicators and scenarios are decision-useful
clarity: 15/15 - concise and readable
```

The 95/100 is a **structural** score. It does not assert that the memo is correct. It says the memo is well-shaped against the protocol.

## Step 3 — Validate the evidence pack

```bash
agenda-intelligence validate-evidence examples/agenda-projections/live-source-backed-memo.evidence.json
```

Output (real):

```text
OK: evidence pack validates
```

## Step 4 — Score with the evidence pack attached

```bash
agenda-intelligence score \
  examples/agenda-projections/live-source-backed-memo.brief.json \
  --evidence examples/agenda-projections/live-source-backed-memo.evidence.json
```

Output (real):

```text
score: 83/100
note: Heuristic structural/evidence-discipline score; does not verify factual truthfulness.
relevance: 25/25 - clear topic, change, and affected actors
evidence_support: 9/25 - evidence_mode=live_source_backed; claims supported: 3/5 supported, 0/5 partially, 2/5 unsupported; unsupported_claims=2; required_but_missing_sources=3; retrieved_at present
completeness: 20/20 - all required fields present; optional fields present: 5/5
actionability: 14/15 - watch-next indicators and scenarios are decision-useful
clarity: 15/15 - concise and readable
```

**This is the integration working as intended, not a regression.**

The score drops from 95 to 83 because the evidence pack is **honest** about what is and is not source-backed. Three claims (the OFAC action itself, named jurisdictions, prior January 15 action) are supported. Two claims (regulator response timing, correspondent-partner behavior) are explicitly marked **unsupported** — they are *assessments* in the memo, not facts. The pack also lists three `required_but_missing_sources` (live SDN lookup, prior press release, EU/UK consolidated lists).

A composition that hides the unsupported assessments would score higher and would **violate this skill's evidence rules**. The lower-but-honest score is the desired outcome.

## Step 5 — MCP transport (optional)

For an MCP-aware agent (Claude Code, Cursor, Codex with MCP, etc.), get the stdio config:

```bash
agenda-intelligence mcp-config
```

Output (real):

```json
{
  "mcpServers": {
    "agenda-intelligence": {
      "command": "agenda-intelligence-mcp"
    }
  }
}
```

The MCP server exposes the same operations (`validate_brief`, `validate_evidence`, `score_output`, `get_protocol`, `list_lenses`, `get_lens`, `source_plan`). An agent using Global Think Tank Analyst as its system instruction can call these tools mid-loop to validate its own draft before returning it.

## Honest finding: scoring on raw markdown

`agenda-intelligence score` on a raw GTTA-style memo file is **not** the right path:

```bash
agenda-intelligence score examples/live-source-backed-memo.md
# Not a before/after example: missing ['## Before: generic agent output', '## After: with Agenda-Intelligence.md']
```

The markdown scorer expects the Agenda Intelligence MD `before/after` markdown shape, not the GTTA memo shape. Use the JSON projection path (Step 2 onward) for GTTA memos. This is the correct, current behavior of the CLI as of 2026-05-08; verify against `agenda-intelligence --help` for newer versions.

## What this composition does and does not catch

**It catches:**

- Missing required brief fields (validate-brief).
- Schema-invalid evidence packs (validate-evidence).
- Memos that label themselves `live_source_backed` but have no evidence pack (the score will reflect it).
- Evidence packs that pad the supported/unsupported ratio dishonestly (the score reflects the ratio).
- Missing watch-next indicators or scenario detail (relevance / actionability lines).

**It does not catch:**

- Whether the cited sources actually say what the claim asserts.
- Whether the assessments are *correct*.
- Whether the chosen scenarios are exhaustive or well-calibrated.
- Whether the analyst applied appropriate judgment to a specific real-world decision.

For all of those, you still need a human reviewer with subject-matter expertise.

## See also

- [`agenda-intelligence-md.md`](agenda-intelligence-md.md) — recipe overview and field mapping.
- [`live-source-backed-memo.md`](../../examples/live-source-backed-memo.md) — the source memo used in this demo.
- [`live-source-backed-memo.brief.json`](../../examples/agenda-projections/live-source-backed-memo.brief.json) — the JSON projection.
- [`live-source-backed-memo.evidence.json`](../../examples/agenda-projections/live-source-backed-memo.evidence.json) — the evidence pack.
