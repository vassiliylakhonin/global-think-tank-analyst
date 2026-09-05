# Claude Code MemoArtifact declared-behavior replication

This is the first cross-model-family execution of
`gtta-artifact-behavior-eval@1.0.0`. It uses the same frozen cases,
expectations, `gtta.memo@1.0` output contract, and deterministic scorer as the
Gemini run.

## Execution record

- Runner: Claude Code 2.1.246
- Model: `claude-opus-4-6`
- Recorded settings: extended thinking enabled, default temperature
- Isolation: one fresh subagent per sample
- Seed: `20260906`
- Samples: 24
- Request SHA-256:
  `cc296b8066b6b6c840c8ee3c4856a22659a7e78c38241f0fadaef04739b84304`
- Output SHA-256:
  `e933a033ba0a1f414159fb389fedbb3d787216879bfb5f51ded3b316522e4c46`
- Skill SHA-256:
  `fbf1f2c2957c0fa7701aabbc4484de954726311ee9c7f74f3b8979837117d57a`
- Expectation-file SHA-256:
  `d9dfe0571be3ebfc7d2582da11a55f4a5f456cdd4c53a8203cbaf3140dbe91ad`
- Prompt/scorer schema SHA-256:
  `fc008c964f895e0efb1945664c00c1254c6c7ae532dc434a37283f4ef7b39848`

The operator reported that each subagent read only its own task and that no
responses were manually corrected. Five samples were retried because their
first attempts ended with rate-limit errors before an output was saved. The
private mapping, expectations, and scorer remained uninspected until all 24
responses were present.

The generated metadata initially retained the Antigravity template's runner
name. Before publication it was corrected to `Claude Code 2.1.246`; model
outputs and their hashes were not changed. The deterministic report was then
regenerated so its embedded metadata matches the execution record.

Independent checks confirmed 24 unique, non-empty, single-object JSON
responses, exact ID coverage across requests, outputs, and private mapping,
matching hashes, and byte-for-byte score reproduction.

## Result

| Arm | Structural pass | Declared-behavior pass | Combined pass | Expectation failures |
|---|---:|---:|---:|---:|
| Baseline | 12 / 12 (100%) | 0 / 12 (0%) | 0 / 12 (0%) | 12 samples |
| Skill | 11 / 12 (91.7%) | 3 / 12 (25.0%) | 3 / 12 (25.0%) | 8 structurally valid samples |

The skill arm again has the higher declared-behavior pass rate, but the
observed difference is `+25.0` percentage points rather than Gemini's `+41.7`.
This replicates direction only. It does not replicate the earlier magnitude or
show strong absolute contract adoption: only three skill samples passed.

The one structural failure was a skill-arm `central-bank-opinion` artifact
whose source-backed claim omitted `source_refs`. Baseline produced 31 behavior
findings; skill produced 11 findings including the structural failure. Missing
claim kinds were the most common issue in both arms. Baseline also omitted all
`verify` flags and frequently omitted the preregistered decision-option
minimums.

Descriptive totals show 84 versus 109 basis-linked claims, 0 versus 14 verify
flags, 17 versus 31 options, and 39 versus 40 indicators for baseline and
skill respectively. These counts do not establish analytical quality.

## Freshness

Freshness passed against all seven earlier published runs with no exact or
near duplicates. The highest relevant structured-run sequence similarity was
`0.449882`; the highest shared-line ratio was `0.394737`, below the disclosed
`0.90` and `0.80` thresholds. Against the prior declared-behavior Gemini run,
the maxima were `0.408148` and `0.363636`.

Freshness is heuristic and cannot prove independent generation.

## Interpretation limits

This is cross-model-family evidence that the observed direction is not unique
to the Gemini run. The small paired suite, one output per arm/case, retries,
model-family sensitivity, and deterministic count rubric prevent a stable
effect-size or causal claim. The scorer does not assess truth, relevance,
reasoning quality, source support, decision quality, or usefulness. External
practitioner usefulness remains U0.
