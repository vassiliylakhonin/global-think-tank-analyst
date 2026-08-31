# Method-contract checker

`gtta check-contract` runs deterministic preflight checks on observable parts
of the Policy Risk Memo Architect method. Each finding has a stable rule ID and
severity, and the report records its ruleset version.

This is a deliberately narrow interface:

- Global Think Tank Analyst checks method declarations, provenance-tag
  presence, likely untagged claims, explicit confidence, selected mode shape,
  and empty generic advice. Exact per-claim accounting uses the structured
  [`MemoArtifact`](memo-artifact.md) interface.
- Agenda Intelligence MD checks the evidence-packet seam: claim/source
  references, declared quotes, lexical support, unmatched numbers, and packet
  completeness.
- Neither checker establishes factual truth. Human review remains required.

## Usage

```bash
gtta check-contract memo.md --mode B
gtta check-contract memo.md --mode B --json
cat memo.md | gtta check-contract - --mode B
```

The command exits non-zero only when an `error` finding exists. Warnings expose
possible method-shape problems without claiming that a deterministic heuristic
understands analytical quality.

## Ruleset `gtta-method-contract@1.2.1`

| Rule | Severity | Checks |
|---|---|---|
| GTTA001 | error | Memo text is not empty |
| GTTA002 | error | Evidence mode is declared |
| GTTA003 | error | Evidence mode is one of the canonical four values |
| GTTA004 | error | At least one Axis A provenance tag is present outside Mode F |
| GTTA005 | warning | An inference or analyst-judgment tag is present outside Mode F |
| GTTA006 | warning | Confidence uses an explicit Low / Moderate / High label outside Mode F |
| GTTA007 | warning | Deeper modes state what would change the judgment |
| GTTA008 | warning | Requested mode output markers are visible |
| GTTA009 | warning | Generic advice is replaced by an observable trigger |
| GTTA010 | warning | A likely material prose or table-cell claim has an inline Axis A provenance tag |

The rules intentionally do not require URLs to resolve, decide whether a cited
source supports a claim, forbid citations on inferences, or treat high
confidence under `reasoning-only` as an automatic error. Those judgments are
not deterministic consequences of the method contract.

GTTA010 is intentionally a warning: Markdown claim boundaries are heuristic.
Use `gtta check-artifact` when exact ledger coverage and cross-reference
validation are required.

Version 1.2.0 reduces layout noise without relaxing claim coverage. Recipient
and sender metadata, direct questions, Markdown table headers, and identifier
columns such as Option or Scenario are treated as layout. Claim-bearing cells
remain checked independently and their warning identifies the table column.
Mode-marker checks accept narrow equivalents such as `Scenario Planning` for
`Scenarios` and `What to Watch` for `Indicators`.

Version 1.2.1 recognizes `Evidence Evaluation Matrix` as a narrow Mode G
equivalent of `Evidence Matrix`. Rule IDs, severities, and claim-warning
coverage are unchanged.

The versioning and automated gate for the stable v1 interface are documented
in [`contract-release-criteria.md`](contract-release-criteria.md).
