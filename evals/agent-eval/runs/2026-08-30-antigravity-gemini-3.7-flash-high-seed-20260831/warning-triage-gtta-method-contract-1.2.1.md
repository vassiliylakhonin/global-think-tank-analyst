# Warning triage — ruleset 1.2.1

This triage reviews the 12 skill-arm GTTA010 warnings in the frozen-output
`gtta-method-contract@1.2.1` rescore. It does not edit the generated outputs or
claim that the underlying analysis is factually correct.

## Findings

| Case | Line | Class | Disposition |
|---|---:|---|---|
| ai-governance-cloud | 53 | Recommendation lead-in | Actionable: “should track” is analytical content and needs provenance |
| board-options-source-conflict | 53 | Recommendation lead-in | Actionable: the required indicators are an analytical recommendation |
| board-options-source-conflict | 65 | Recommendation lead-in | Actionable: the proposed Board requirement needs provenance |
| cbam-enforcement | 53 | Recommendation lead-in | Actionable: monitoring advice needs provenance |
| central-bank-opinion | 60 | Recommendation lead-in | Actionable: indicator-selection advice needs provenance |
| conflicting-policy-dates | 60 | Recommendation lead-in | Actionable: monitoring advice needs provenance |
| critical-minerals-rumor | 33 | Recommendation lead-in | Actionable: trigger-selection advice needs provenance |
| export-controls-permanence | 40, column 1 | Red-team premise cell | Actionable: the analyst-decomposed premise needs `[analyst-judgment]` |
| hormuz-energy-shock | 53 | Recommendation lead-in | Actionable: monitoring advice needs provenance |
| partner-risk-manageable | 42, column 1 | Red-team premise cell | Actionable: the analyst-decomposed premise needs `[analyst-judgment]` |
| quick-sanctions-corridor-triage | 33 | Recommendation lead-in | Actionable: monitoring advice needs provenance |
| trade-framework-exporter | 60 | Recommendation lead-in | Actionable: indicator-selection advice needs provenance |

## Resulting method change

The runtime method now states explicitly that a recommendation lead-in remains
claim-bearing when it ends with a colon before a list. It also distinguishes a
neutral table row identifier from a quoted or summarized red-team premise:
input-supplied premises use `[user-provided]`; analyst-decomposed premises use
`[analyst-judgment]`.

The separate GTTA008 finding in the immutable ruleset-1.2.0 report was a
checker false positive. Ruleset 1.2.1 recognizes `Evidence Evaluation Matrix`
as a narrow Mode G alias, removing that warning without relaxing provenance
coverage.
