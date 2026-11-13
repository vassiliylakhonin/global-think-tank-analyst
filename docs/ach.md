# Deterministic ACH matrix

`gtta ach matrix.json` (or `gtta ach -` on stdin) accepts a complete, manually
supplied evidence-by-hypothesis matrix. No LLM assigns or grades cells.

```json
{"schema_version":"gtta.ach@1.0","hypotheses":["H1","H2"],"evidence":["E1"],"matrix":{"E1":{"H1":"inconsistent","H2":"consistent"}}}
```

Allowed cells: `consistent`, `inconsistent`, `neutral`, `unknown`. Missing cells,
extra IDs, duplicate IDs and invalid cells are errors. Output ranks by number of
inconsistencies, ascending. Ties share competition rank, preserving input order.
The report names contradictory evidence, unknowns and assessed-cell counts.

A hypothesis with mostly unknown cells can have zero inconsistencies. That does
not make it likely: inspect coverage and human judgments. Evidence independence,
diagnosticity and source quality are not evaluated. No probabilities, truth or
analytical-quality improvement are claimed. This is a calculator for a supplied
matrix, not an automated ACH analyst. Existing Mode G prose guidance is unchanged.
