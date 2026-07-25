# Maturity framework and portfolio canon alignment

Which framework this repo measures itself against, and why it differs from the vertical-specialist siblings.

Referenced from `AGENTS.md`.

This repo uses [`VALIDATION_PLAN.md`](../VALIDATION_PLAN.md) as its maturity framework. The target outcome is **practitioner feedback** on a small number of reviewable case packets, recorded under [`reviews/`](../reviews/) only after a real external reviewer responds. Author self-review does not count as external validation.

The sibling vertical-specialist repos in this portfolio (`central-asia-caspian-hybrid-intelligence-skill`, `gulf-middle-east-hybrid-intelligence-skill`) use a different framework — a two-bar Definition of Done with explicit Bar 1 (early but credible) and Bar 2 (agent-validated specialist resource) criteria, encoded as a `STATUS.md` file in each repo. Bar 2 accepts self-scored agent-eval delta cases plus source-anchored examples; practitioner review is the optional B2.8 layer.

The two frameworks are not interchangeable and not in conflict:

- The vertical-specialist Bar 1 / Bar 2 canon centers on **source-anchored majority** (B2.1) and **evidence-mode mapping through `analyze`** (B2.3). Both criteria are designed around region-deep specialist examples that cite primary regulator / IFI / IMO / FATF sources. They do not map cleanly onto a horizontal reasoning-method skill, where the asset is memo shape across many domains rather than depth in one source-rich region.
- GTTA's `VALIDATION_PLAN.md` is **stricter on the practitioner-review axis** (self-review explicitly does not count) and **looser on the per-criterion structural axis** (it does not require a 50%-source-anchored ratio across examples). This reflects what an honest maturity claim looks like for a horizontal method skill, not a vertical specialist.
- Both frameworks share the same **agent-eval delta methodology** ([agenda-intelligence-md/docs/agent-eval-methodology.md](https://github.com/vassiliylakhonin/agenda-intelligence-md/blob/main/docs/agent-eval-methodology.md)) and the same **honesty rules** (no self-scored aggregate benchmarks, no fabricated metrics, no real-use claims without attributable evidence).

When this repo or its case studies refer to "the canon" or "the Definition of Done", they refer to `VALIDATION_PLAN.md`, not to vertical Bar 1 / Bar 2. Portfolio-level write-ups must state which framework they are referencing, per repo, to avoid implying that "agent-validated" in a vertical context and "early but credible" in the horizontal context mean the same thing.
