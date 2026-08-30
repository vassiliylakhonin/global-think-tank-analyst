# MemoArtifact interface

`MemoArtifact` is the canonical machine-readable handoff for a GTTA memo. It
keeps atomic claims, their provenance, and their use in the human-readable memo
inside one versioned object. CLI and MCP are adapters over the same Python
implementation.

Schema version: `gtta.memo@1.0`.

## Why this interface exists

Markdown is useful to people but ambiguous to validators. A checker can warn
that a sentence appears untagged, but it cannot reliably decide where one claim
ends or whether a table cell introduces a second claim. `MemoArtifact` makes
that accounting explicit:

- each atomic ledger claim has a stable ID, kind, provenance, and optional
  source references;
- derived claims can name the claims on which they depend;
- narrative blocks, options, and indicators link back to ledger claims;
- mode-specific sections and deeper-mode requirements are validated together;
- rendering adds provenance tags and `[basis: ...]` links to Markdown;
- structured Decision and Change condition fields render with explicit layout
  labels so the Markdown checker does not confuse them with untagged claims.

The artifact validator checks declarations and cross-references. It does not
fetch sources, determine whether a source supports a claim, or establish
factual truth. Agenda Intelligence MD owns the downstream evidence-packet seam.

## Minimal Mode B example

```json
{
  "schema_version": "gtta.memo@1.0",
  "artifact_id": "pilot-001",
  "title": "Reversible pilot",
  "question": "Should the operator run a limited pilot?",
  "decision": "Choose whether to authorize a 30-day pilot.",
  "audience": "Operating committee",
  "time_horizon": "30–90 days",
  "mode": "B",
  "evidence_mode": "reasoning-only",
  "bottom_line": {
    "text": "A reversible pilot is preferable to a full rollout.",
    "claim_ids": ["c2"]
  },
  "claims": [
    {
      "claim_id": "c1",
      "text": "The decision can be staged without committing the full budget.",
      "kind": "assumption",
      "provenance": "inference",
      "confidence": "Moderate"
    },
    {
      "claim_id": "c2",
      "text": "A limited pilot preserves more option value than immediate rollout.",
      "kind": "assessment",
      "provenance": "analyst-judgment",
      "basis_claim_ids": ["c1"],
      "confidence": "Moderate"
    }
  ],
  "sections": {
    "actors": {
      "text": "The operator values speed while the committee values reversibility.",
      "claim_ids": ["c1"]
    }
  },
  "options": [
    {
      "option_id": "o1",
      "title": "Authorize a limited pilot",
      "benefit": "Tests assumptions before scaling.",
      "downside": "Delays full rollout.",
      "conditions": "Use a measurable exit criterion.",
      "basis_claim_ids": ["c1", "c2"]
    }
  ],
  "confidence": "Moderate",
  "key_unknowns": ["Whether pilot conditions reproduce full-scale constraints."],
  "change_conditions": ["Evidence that even a pilot is irreversible."],
  "limitations": ["No external sources were consulted."]
}
```

## Commands

```bash
gtta artifact-schema
gtta check-artifact memo.json
gtta check-artifact memo.json --json
gtta render-artifact memo.json > memo.md
```

For Python integrations, use `MemoArtifact`, `check_memo_artifact()`,
`get_memo_artifact_schema()`, and `render_memo_artifact()` from `gtta`. MCP
exposes the same schema, validation, and rendering operations.

## Compatibility

Within `gtta.memo@1.x`, existing required fields and enum meanings remain
stable. Additive optional fields may be introduced. Removing a field, changing
its meaning, or adding a new required invariant requires `gtta.memo@2.0`.

The old models in `gtta.schemas` remain compatibility types but are no longer
the canonical memo interface.
