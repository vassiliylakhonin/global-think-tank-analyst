# Evaluation suite commitments

These files preregister an evaluation suite before its first model outputs are
generated. A commitment records hashes of the exact cases, hidden declared-
behavior expectations, generated requests, runtime skill, and artifact schema.
It does not disclose the hidden expectations.

For a holdout run, commit and push the commitment before generation. Keep the
case source, expectation source, and private mapping outside the model context
until every response has been saved. When the run is published, add those
frozen inputs so another person can reproduce every hash and score.

This is an audit mechanism, not proof that generation was independent or that
the benchmark measures analytical quality. Git history establishes when this
repository recorded the commitment; execution isolation remains procedural.

## Fulfilled commitment

- [`2026-09-05-artifact-behavior-holdout-v1.json`](2026-09-05-artifact-behavior-holdout-v1.json)
  binds `gtta-agent-eval-holdout@1.0.0`: 10 new cases / 20 paired samples,
  seed `20260907`. The frozen inputs and first completed run are now published
  [together](../runs/2026-09-05-antigravity-gemini-3.8-flash-high-artifact-behavior-holdout-v1-seed-20260907/).
