# Gemini structured MemoArtifact replication — protocol 1.1.0

This is the fresh post-correction replication of the first structured
`MemoArtifact` run. Protocol `gtta-artifact-eval@1.1.0` gives both arms the
same exact Mode-to-section-key map and explicitly separates `ClaimKind` from
provenance.

## Execution record

- Runner: Antigravity 2.11.0
- Model: Gemini 3.7 Flash (High)
- Recorded generation settings: `{"thinking": "high"}`
- Seed: `20260904`
- Samples: 24, one isolated fresh context per sample
- Artifact schema: `gtta.memo@1.0`
- Request SHA-256:
  `61b34191605329f1ff1817e4f4b0cbd36f4af3ce9574f79ac2f216dc49cc4516`
- Output SHA-256:
  `5f16690de2fca086660e9c720664a6fbaf8b389d2bc62bd98f4385685e3f0dd4`
- Prompt/scorer schema SHA-256:
  `fc008c964f895e0efb1945664c00c1254c6c7ae532dc434a37283f4ef7b39848`

The operator reported that all tasks ran in fresh isolated contexts, the same
model and settings were used throughout, `private-mapping.json` remained
uninspected until all outputs were saved, and responses were not manually
edited. Independent local checks confirmed 24 non-empty single-object JSON
files, matching hashes, and byte-for-byte score reproduction.

## Result

| Arm | Passed | Pass rate | Parse failures | Interface failures | Expectation failures |
|---|---:|---:|---:|---:|---:|
| Baseline | 12 / 12 | 100% | 0 | 0 | 0 |
| Skill | 12 / 12 | 100% | 0 | 0 | 0 |

The section-key and claim-axis failure classes from protocol 1.0.0 did not
recur. This supports the narrow conclusion that the shared adapter correction
worked in this run. Because both arms reached 100%, this suite has a ceiling
for schema conformance and supplies no positive skill delta.

Descriptive totals differ slightly: skill artifacts contain 61 basis-linked
claims versus 59, four `verify` flags versus zero, and 27 indicators versus
24. These small generated counts are not a quality score and are not treated
as a causal method effect.

## Freshness

Freshness passed against the protocol 1.0.0 run with no exact or near
duplicates. Maximum observed whole-text sequence similarity was `0.491779`;
maximum shared-line ratio was `0.520468`, below the disclosed `0.90` and
`0.80` thresholds. This heuristic can detect likely reuse but cannot prove
independent generation; the execution record remains necessary evidence.

## Interpretation limits

The scorer checks JSON parsing, declared artifact invariants, and expected Mode
and evidence-mode matching only. It does not evaluate truth, source support,
analytical depth, decision quality, or practitioner usefulness. External
usefulness remains U0.
