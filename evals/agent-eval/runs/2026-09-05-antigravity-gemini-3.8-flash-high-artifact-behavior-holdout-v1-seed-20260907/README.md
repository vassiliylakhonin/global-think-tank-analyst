# Gemini 3.8 MemoArtifact declared-behavior holdout

This is the first execution of the preregistered broader-domain suite
`gtta-agent-eval-holdout@1.0.0` under
`gtta-artifact-behavior-eval@1.0.0`. It contains 10 new paired cases across
Modes A-G, including the first Mode F case. The exact suite, expectations,
requests, skill, schema, and seed were hash-committed in Git before generation.

## Execution record

- Runner: Antigravity 2.12.2
- Model: `Gemini 3.8 Flash (High)`
- Recorded settings: `{"thinking": "high"}`
- Seed: `20260907`
- Samples: 20 (10 paired cases)
- Request SHA-256:
  `dfb653285eb9c0d30e3b98853128fffb440aa59610abe3c0939f6d90d21ad478`
- Output SHA-256:
  `c4b22f1c2b94fe313e04e999118f99a14f3ee18658b47e44a1a3ed384dfaa888`
- Report SHA-256:
  `0636332627684bc66a4890ba4e7ebf965a377f56f495b944068d2740d069590c`

The generated commitment matches the version committed before execution:

| Bound input | SHA-256 |
|---|---|
| Cases | `a16d6d26760cea61b38b0f59f130e8372c5435d603161745f162ba5bf6a39647` |
| Expectations | `3f87904a74c31345c103656a110eae1f3087ce94bc01fefc304de3f6f6bac54d` |
| Requests | `dfb653285eb9c0d30e3b98853128fffb440aa59610abe3c0939f6d90d21ad478` |
| Skill | `fbf1f2c2957c0fa7701aabbc4484de954726311ee9c7f74f3b8979837117d57a` |
| Artifact schema | `fc008c964f895e0efb1945664c00c1254c6c7ae532dc434a37283f4ef7b39848` |

Independent repository checks confirmed 20 unique, non-empty, single-object
JSON responses, exact ID coverage, byte equality between raw saved responses
and imported outputs, aggregate reconciliation, and byte-for-byte score
reproduction.

## Execution caveat

The operator log records one initial baseline subagent being stopped while its
delivery setup was corrected, then started again before an output was accepted.
The imported metadata says `retry count: 0`; that is accurate only if retries
means failed tasks in the final accepted batch, not all orchestration attempts.
The final saved response came from the restarted context, so sample coverage is
unchanged, but the discrepancy is retained rather than silently corrected.

The operator inferred arm identity from the request system text in order to
configure two no-tool subagent definitions. That does not change the intended
prompt difference—the skill text is necessarily present only in the skill
arm—but it means execution orchestration was not arm-blind. Responses were
copied or extracted from Antigravity transcripts into the raw files. Their
equality with imported outputs is verified; absence of manual semantic edits
cannot be proven cryptographically from the retained repository artifacts.

## Result

| Arm | Structural pass | Declared-behavior pass | Combined pass | Expectation failures |
|---|---:|---:|---:|---:|
| Baseline | 10 / 10 (100%) | 0 / 10 (0%) | 0 / 10 (0%) | 10 samples |
| Skill | 10 / 10 (100%) | 0 / 10 (0%) | 0 / 10 (0%) | 10 samples |

Finding counts:

| Code | Baseline | Skill |
|---|---:|---:|
| `ARTIFACTB001` — missing required claim kind | 2 | 3 |
| `ARTIFACTB002` — missing required provenance | 0 | 1 |
| `ARTIFACTB007` — too few `verify: true` claims | 10 | 8 |

Both arms achieved exact structural conformance. Neither arm passed a complete
case-level behavior expectation. The dominant failure is highly concentrated:
baseline emitted zero verification flags; skill emitted four, but eight skill
cases still fell below their preregistered minimum. Descriptive totals otherwise
remain close: 109 versus 113 claims, 77 versus 74 basis-linked claims, 30 versus
28 options, and 28 versus 29 indicators. These totals are not quality scores.

## Interpretation

This holdout does not reproduce the positive combined-pass difference observed
on the disclosed 12-case suite. It shows that schema conformance generalizes to
the new domains for this model/run, while adoption of the full declared-
behavior contract does not. The result argues against a broad claim that the
skill reliably transfers every runtime instruction into `MemoArtifact` fields.

No cross-run freshness report is produced because the earlier runs have a
different case/arm set and the verifier deliberately rejects incomparable
sets. Pre-run Git commitment and fresh-context execution are the applicable
controls; neither proves independence.

This deterministic score does not assess truth, source support, reasoning
quality, decision quality, causality, or practitioner usefulness. The suite is
small, the threshold is conjunctive, and the execution caveats above reduce
procedural confidence. External usefulness remains U0.
