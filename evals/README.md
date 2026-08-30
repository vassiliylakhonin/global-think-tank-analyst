# Evaluation aids

Lightweight, **human review** materials for memos produced with the Global Think Tank Analyst skill.

These are not a validated benchmark. They do not produce a number you can compare to other systems. They are starter aids for a human reviewer who wants to ask consistent questions of a strategic-risk memo.

For machine-readable validation, scoring, and evidence audit, see the companion project [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md).

| File | Purpose |
|---|---|
| [checklist.md](checklist.md) | Yes/no questions a reviewer asks of any memo |
| [failure-modes.md](failure-modes.md) | Common ways memos go wrong, with diagnostic cues |
| [rubric.md](rubric.md) | Starter scoring rubric across eight dimensions |
| [adversarial/](adversarial/README.md) | Stress cases: inputs designed to fail predictably (prompt-injection in sources, conflicting evidence, source mislabeling) |
| [agent-eval/](agent-eval/) | With/without structural delta cases (agent-eval methodology), plus rule-level canon evals |
| [skill-improvement/](skill-improvement/README.md) | Validation-gated checks for proposed edits to runtime skill instructions |

Treat the rubric as opinionated and adjustable. It is not a standard. The adversarial cases are the negative counterpart to the checklist: not "did the memo look good," but "did the skill refuse the things it should refuse."

The paired harness in `agent-eval/` can prepare and deterministically score 12
same-task baseline/skill samples. Its output is method-contract evidence only,
not a factual or practitioner benchmark.
