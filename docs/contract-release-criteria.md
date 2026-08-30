# Method-contract release criteria

The `gtta-method-contract@1.x` label means the checker interface is stable. It
does **not** mean GTTA has been externally validated or that a passing memo is
factually correct.

## Stability promise

Within contract major version 1:

- existing rule IDs keep their meaning and severity;
- JSON report fields remain backward compatible;
- a new warning rule may be added in a minor release;
- a new error rule or changed error semantics requires a major release;
- heuristic refinements that change findings in either direction require a
  documented ruleset version change and regression cases.

## Automated release gate

A package release may expose contract v1 only when all of the following pass:

1. Unit and integration tests.
2. Repository checks, including runtime-resource drift.
3. Every canonical example has a supported evidence mode and no contract
   `error` finding.
4. The 10-20 case paired agent-eval suite validates structurally.
5. The built wheel exposes the same resources, CLI, checker, `MemoArtifact`
   schema/renderer, and MCP tools as the source tree.

The paired agent-eval does not have to claim a positive quality delta for a
software release. If it is executed and results are published, the exact model,
settings, skill hash, scorer version, and self-scoring limitation must be
recorded.

## Validation status

External practitioner review remains the strongest usefulness test in
`VALIDATION_PLAN.md`, but it is currently unavailable. That absence does not
block honest software releases; it blocks claims such as "practitioner
validated", "production proven", or "operationally reliable".
