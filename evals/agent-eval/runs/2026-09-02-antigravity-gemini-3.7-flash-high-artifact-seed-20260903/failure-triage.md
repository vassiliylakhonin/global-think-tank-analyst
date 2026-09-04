# Failure triage

## Observed failure classes

| Failure class | Baseline samples | Skill samples |
|---|---:|---:|
| Missing exact Mode section keys | 2 | 10 |
| Invalid `claim.kind = "inference"` | 0 | 1 |

The structured validator behaved as documented. Valid artifacts using the
canonical keys passed, including 10 baseline samples and one skill sample.

## Root cause

`MemoArtifact.sections` is a dictionary, so its JSON Schema describes the
value shape but cannot encode which dictionary keys are required for each
Mode. Those cross-field invariants live in the Pydantic model validator. The
`1.0.0` output contract told the model to satisfy Mode-specific rules but did
not list the exact keys.

The runtime method supplies human-facing headings such as “Main risks” and
“Actors and incentives”. In 10 skill samples the model copied variants of
those headings into `sections`, where the interface instead requires
`main_risks` and `actors`. One sample also conflated the Axis A provenance
value `inference` with the separate `ClaimKind` enum.

## Correction

`gtta-artifact-eval@1.1.0` adds the exact, case-sensitive section-key map for
Modes A-G and explicitly separates the allowed `claim.kind` and
`claim.provenance` values. The same correction is given to both arms. The
schema and validator are not weakened, and old outputs are not normalized or
edited after generation.

This diagnosis predicts that a fresh `1.1.0` run will remove these two failure
classes. That prediction requires a new isolated run; it is not established by
the prompt edit alone.
