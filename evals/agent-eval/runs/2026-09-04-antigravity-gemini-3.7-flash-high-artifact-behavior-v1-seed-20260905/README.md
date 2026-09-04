# Gemini MemoArtifact declared-behavior run — protocol 1.0.0

This is the first execution of
`gtta-artifact-behavior-eval@1.0.0`. It retains the shared
`gtta.memo@1.0` output contract from the corrected structured protocol, then
checks preregistered case-specific minimums over model-declared fields.

## Execution record

- Runner: Antigravity 2.11.0
- Model: Gemini 3.7 Flash (High)
- Recorded generation settings: `{"thinking": "high"}`
- Seed: `20260905`
- Samples: 24, one isolated fresh context per sample
- Artifact schema: `gtta.memo@1.0`
- Request SHA-256:
  `3e6609ac79834b87c03eb918c2468a1c3a44556d2a6835db313ca7305a3d572e`
- Output SHA-256:
  `85ed9409259574340718a41f84067ca5eef6dfa3c715b7e69367e5a434632a1c`
- Skill SHA-256:
  `fbf1f2c2957c0fa7701aabbc4484de954726311ee9c7f74f3b8979837117d57a`
- Expectation-file SHA-256:
  `d9dfe0571be3ebfc7d2582da11a55f4a5f456cdd4c53a8203cbaf3140dbe91ad`
- Prompt/scorer schema SHA-256:
  `fc008c964f895e0efb1945664c00c1254c6c7ae532dc434a37283f4ef7b39848`

The operator reported that the same model and settings were used in fresh
isolated contexts, no paid or external API was used, and the private mapping,
expectations, and scorer remained uninspected until all responses were saved.
Independent local checks confirmed 24 unique non-empty single-object JSON
responses, exact request/output/mapping ID coverage, matching hashes, and
byte-for-byte score reproduction.

## Result

| Arm | Structural pass | Declared-behavior pass | Combined pass | Expectation failures |
|---|---:|---:|---:|---:|
| Baseline | 12 / 12 (100%) | 3 / 12 (25.0%) | 3 / 12 (25.0%) | 9 samples |
| Skill | 12 / 12 (100%) | 8 / 12 (66.7%) | 8 / 12 (66.7%) | 4 samples |

The observed declared-behavior difference is `+41.7` percentage points for the
skill arm in this run. It breaks the earlier schema-only ceiling and supports
the narrow conclusion that the skill arm more often satisfied the frozen
declaration minima. One execution on one model does not establish a stable or
general causal effect.

Baseline produced 14 findings across nine failed samples: seven
`ARTIFACTB001`, five `ARTIFACTB007`, one `ARTIFACTB003`, and one
`ARTIFACTB004`. Skill produced five findings across four failed samples: three
`ARTIFACTB001`, one `ARTIFACTB006`, and one `ARTIFACTB007`. The common gaps
were missing declared unknowns or assumptions and missing `verify` flags; the
skill arm also missed one scenario-case indicator minimum.

Descriptive totals show 45 versus 65 basis-linked claims, 9 versus 12 verify
flags, 25 versus 30 options, and 26 versus 28 indicators for baseline and
skill respectively. These generated counts are not quality scores.

## Freshness

Freshness passed against both earlier structured Gemini runs with no exact or
near duplicates. Against protocol 1.0.0, maximum sequence similarity was
`0.511594` and maximum shared-line ratio was `0.480519`. Against the corrected
protocol 1.1.0 run, the maxima were `0.572962` and `0.570588`, below the
disclosed `0.90` and `0.80` thresholds.

The detector is heuristic: passing can identify no likely reuse under its
rules but cannot prove independent generation.

## Interpretation limits

The scorer counts model-declared categories and links. It does not judge
whether claims are distinct, relevant, true, well reasoned, source-supported,
or useful. This is author-operated method-contract evidence, not external
validation. Practitioner usefulness remains U0.
