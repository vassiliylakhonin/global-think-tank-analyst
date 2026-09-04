# Structured MemoArtifact eval

The structured path measures whether a model can produce the canonical
`gtta.memo@1.0` object for the same frozen 12 cases used by the Markdown
paired eval. It complements the heuristic method-contract score; it does not
replace it.

## Fair comparison

Both arms receive:

- the same strategic-risk baseline instruction;
- the same requested Mode and evidence mode;
- the same serialized JSON Schema;
- the same non-schema interface invariants;
- the same instruction to return one raw JSON object.

Only the skill arm receives the GTTA runtime method. Sample IDs are opaque and
the arm mapping stays private until all outputs have been saved.

## What passes

A sample passes only when all of the following are true:

1. the response parses as one JSON object;
2. it validates as `gtta.memo@1.0`, including claim-ledger, reference,
   dependency, orphan, evidence-mode, and Mode-specific invariants;
3. its declared Mode matches the benchmark case;
4. its declared evidence mode matches the benchmark case.

The report also records descriptive counts for claims, source-backed claims,
basis-linked claims, verify flags, options, and indicators. These counts are
not quality scores.

## Declared-behavior suite

Protocol `gtta-artifact-behavior-eval@1.0.0` adds a second, deliberately
separate score after structural validation. Its preregistered expectations are
frozen in [`artifact-behavior-expectations.json`](artifact-behavior-expectations.json).
They set case-specific minimum counts for declared claim kinds and provenance,
basis-linked claims, bottom-line support, options, indicators, verification
flags, key unknowns, and change conditions.

The expectations are not included in model requests and are copied into the
private mapping for deterministic reproduction. During execution, the runner
must not inspect the private mapping, scorer, or expectation file until all 24
responses have been saved. The report keeps `structural_pass_rate`,
`behavioral_pass_rate`, and combined `pass_rate` separate so a formatting
failure cannot be mistaken for a behavioral shortfall.

This suite measures adoption of declared method behaviors only. Counts cannot
show that claims are distinct, relevant, true, well reasoned, source-supported,
or useful. The suite is designed to avoid the 100%/100% schema ceiling, not to
turn a deterministic checker into a quality judge.

## Run without a paid API

```bash
python3 scripts/agent_eval.py prepare-artifact \
  /tmp/gtta-artifact-eval \
  --seed 20260904

# Fill run-metadata.template.json and execute every opaque task in a fresh
# Antigravity conversation, saving raw .json responses as instructed.

python3 scripts/agent_eval.py import-antigravity \
  /tmp/gtta-artifact-eval \
  /tmp/gtta-artifact-eval/antigravity-responses \
  --metadata /tmp/gtta-artifact-eval/run-metadata.template.json \
  --output /tmp/gtta-artifact-eval/outputs.jsonl

python3 scripts/agent_eval.py score-artifact \
  /tmp/gtta-artifact-eval \
  /tmp/gtta-artifact-eval/outputs.jsonl \
  --report /tmp/gtta-artifact-eval/report.json
```

For the declared-behavior suite, use the parallel commands:

```bash
python3 scripts/agent_eval.py prepare-artifact-behavior \
  /tmp/gtta-artifact-behavior-eval \
  --seed 20260905

# Generate/import the same way, without inspecting the hidden mapping or
# expectation implementation before all responses are saved.

python3 scripts/agent_eval.py score-artifact-behavior \
  /tmp/gtta-artifact-behavior-eval \
  /tmp/gtta-artifact-behavior-eval/outputs.jsonl \
  --report /tmp/gtta-artifact-behavior-eval/report.json
```

The harness makes no model or network calls. A publishable run must retain the
requests, private mapping, raw outputs, run metadata, report, and hashes. A
replication on the same cases must also pass the disclosed freshness gate.

## Interpretation limits

Passing establishes declared structural conformance only. It does not show
that a claim is true, that a source supports it, that the analysis is good, or
that a decision-maker finds it useful. A model can produce a formally valid
but shallow artifact. Human review and downstream evidence-packet checking
remain separate seams.

## Protocol history

- `gtta-artifact-eval@1.0.0` introduced the path but did not enumerate exact
  Mode-specific dictionary keys or explicitly distinguish `ClaimKind` from
  provenance in its non-schema instructions. The first run exposed both gaps.
- `gtta-artifact-eval@1.1.0` gives both arms the exact case-sensitive key map
  for Modes A-G and lists the two claim axes separately. This changes prompts
  and sample IDs, not `gtta.memo@1.0` or the scorer. Its fresh Gemini run passed
  12/12 in both arms, confirming the adapter correction while showing that the
  current schema-conformance pass rate has a ceiling.
- `gtta-artifact-behavior-eval@1.0.0` preserves the shared schema contract but
  adds frozen case-level expectations over declared analytical structure. It
  reports structure and behavior independently and makes no semantic-quality
  claim. Its first fresh Gemini run passed 8/12 skill samples versus 3/12
  baseline after both arms passed 12/12 structural checks.
