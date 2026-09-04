# Gemini structured MemoArtifact run — seed 20260903

This is the first completed `gtta-artifact-eval@1.0.0` paired run over the
frozen 12-case suite. It is intentionally published despite a negative skill
delta because it exposed an interface-adapter defect that the Markdown eval
could not reveal.

## Execution record

- Runner: Antigravity 2.11.0
- Model: Gemini 3.7 Flash (High)
- Recorded generation settings: `{"thinking": "high"}`
- Samples: 24, one isolated fresh context per sample
- Artifact schema: `gtta.memo@1.0`
- Request SHA-256:
  `74d220d43c4a00ad31dd6891503be1cb12e726e2550ea90221c168e53dce179f`
- Output SHA-256:
  `02bde6070972b17a59202a3a86cd5d64cbebf83ddf8fd70130e825cb2e8303c4`
- Prompt/scorer schema SHA-256:
  `fc008c964f895e0efb1945664c00c1254c6c7ae532dc434a37283f4ef7b39848`

The operator reported that `private-mapping.json` was not inspected until all
24 raw JSON responses had been saved and that responses were not manually
edited. The import and scorer both exited with status 0.

## Result

| Arm | Passed | Pass rate | JSON parse failures | Interface failures |
|---|---:|---:|---:|---:|
| Baseline | 10 / 12 | 83.3% | 0 | 2 |
| Skill | 1 / 12 | 8.3% | 0 | 11 |

All 13 findings are `ARTIFACT003`. Ten of the 11 skill failures use
human-readable or Markdown-style section names instead of the exact
case-sensitive machine keys required by `MemoArtifact`. The remaining skill
failure uses `inference` as a claim `kind`; `inference` is a provenance value.
The two baseline failures also omit canonical section keys.

[`failure-triage.md`](failure-triage.md) records the diagnosis and the
versioned prompt correction. The frozen requests, outputs, mapping, metadata,
and original report remain unchanged.

## Interpretation

This run shows that `gtta-artifact-eval@1.0.0` did not adequately translate
the runtime method's human-readable headings into the structured interface.
It does **not** show that the method is analytically worse than the baseline.
Conversely, baseline's 10/12 structural result is not evidence of better
factuality or decision quality.

The scorer checks JSON parsing, declared artifact invariants, and expected Mode
and evidence-mode matching only. It does not evaluate truth, source support,
analytical quality, decision quality, or practitioner usefulness. External
usefulness remains U0.
