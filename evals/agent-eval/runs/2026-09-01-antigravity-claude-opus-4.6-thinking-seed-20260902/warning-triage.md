# Warning triage — Claude replication, ruleset 1.2.2

This bounded review covers the 111 skill-arm warnings in the immutable report.
It does not edit the model outputs or assess whether their substantive claims
are true.

## Count boundary

GTTA010 stops after 25 findings per sample. Three cases reached that cap:
`ai-governance-cloud`, `cbam-enforcement`, and `partner-risk-manageable`.
Consequently, the report contains exactly 110 GTTA010 findings but may omit
additional detectable claims in those three responses.

## Findings by case

| Case | GTTA008 | GTTA010 | Disposition note |
|---|---:|---:|---|
| ai-governance-cloud | 0 | 25 cap | Predominantly claim-bearing table cells without a tag in each cell |
| board-options-source-conflict | 0 | 1 | Untagged summary of the supplied evidence boundary |
| cbam-enforcement | 0 | 25 cap | Untagged scenario premises, implications, and table cells |
| central-bank-opinion | 0 | 3 | Untagged evidentiary caveat, disclaimer, and confidence lead-in |
| conflicting-policy-dates | 0 | 1 | Untagged analytical lead-in |
| critical-minerals-rumor | 0 | 1 | Untagged indicator-selection lead-in |
| export-controls-permanence | 0 | 10 | Untagged target-claim decomposition and watch indicators |
| hormuz-energy-shock | 1 | 8 | Missing explicit Indicators marker plus untagged pathways and table cells |
| infrastructure-attribution | 0 | 10 | Untagged hypothesis definitions and method judgments |
| partner-risk-manageable | 0 | 25 cap | Untagged user-claim decomposition and claim-bearing table cells |
| quick-sanctions-corridor-triage | 0 | 0 | No deterministic warnings |
| trade-framework-exporter | 0 | 1 | Untagged confidence/unknowns lead-in |

Of the 110 GTTA010 findings, 73 identify individual table cells and 37 identify
prose lines. Per-cell warnings are not automatically duplicates: the contract
requires a provenance tag in every claim-bearing cell rather than one tag for
an entire row.

## Interpretation

- The updated instruction against replacing Axis A with `[assumption]`,
  `[unknown]`, or `[scenario]` was followed in all stored warning lines.
- One Mode C response still omitted the required visible Indicators marker;
  scenario content is not a substitute for the required decision-facing
  section.
- Many remaining GTTA010 findings are actionable under the declared method,
  especially untagged table cells, user-provided premises, and analytical
  lead-ins.
- Some layout caveats and disclaimers may be heuristic noise. This review does
  not claim that all 110 findings were individually adjudicated.

Exact claim accounting requires `MemoArtifact`. Raw Markdown warning totals,
especially capped totals, should be treated as diagnostics rather than a
standalone quality score.
