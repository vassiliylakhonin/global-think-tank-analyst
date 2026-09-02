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

## Run without a paid API

```bash
python3 scripts/agent_eval.py prepare-artifact \
  /tmp/gtta-artifact-eval \
  --seed 20260903

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

The harness makes no model or network calls. A publishable run must retain the
requests, private mapping, raw outputs, run metadata, report, and hashes. A
replication on the same cases must also pass the disclosed freshness gate.

## Interpretation limits

Passing establishes declared structural conformance only. It does not show
that a claim is true, that a source supports it, that the analysis is good, or
that a decision-maker finds it useful. A model can produce a formally valid
but shallow artifact. Human review and downstream evidence-packet checking
remain separate seams.
