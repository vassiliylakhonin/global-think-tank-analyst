# Self-runs

Fixed reference outputs of the Global Think Tank Analyst skill against published adversarial cases and other test inputs.

**Status: author self-review. Not external validation.**

Self-runs exist for one reason: to pair every published adversarial case (and, over time, other test inputs) with an observable artifact that shows the skill applied honestly. Without that, the adversarial cases describe the trap and the expected behavior, but no one — author included — can see what a passing memo looks like.

## What this is

- A reference output per case, marked with the date and the model used.
- A pass/fail pass against the case's published criteria, performed by the author.
- An honesty section that names what is missing for the run to count as evidence of robustness.

## What this is not

- Not external validation. The author is the runner. See [`../../VALIDATION_PLAN.md`](../../VALIDATION_PLAN.md) for what external validation requires.
- Not a benchmark. There is no scoring tooling, no held-out test set, no cross-model regression record.
- Not a guarantee of repeatability. A single observation by one model on one prompt is one observation.
- Not a substitute for the adversarial cases themselves. The cases publish the criteria; self-runs are one author's attempt at satisfying them.

## Reading a self-run file

Each file follows this structure:

1. Header — date, case reference, runner, status disclaimer.
2. Prompt used — pasted verbatim from the case Setup block, so the run is reproducible.
3. Skill output — the memo produced.
4. Pass / fail against case criteria — explicit, criterion by criterion.
5. What would change the judgment — what would turn this single observation into evidence.
6. Honesty notes — anything that could be misread as stronger evidence than it is.

## How to add a self-run

1. Pick an adversarial case (or any other published test input) from [`../adversarial/`](../adversarial/).
2. Run it through an agent with `AGENTS.md` + `SKILL.md` + `llms.txt` loaded.
3. Save the result under `YYYY-MM-DD-<case-slug>.md` following the structure above.
4. Do not edit the case file to fit the output. If the output fails a criterion, record the fail and either fix the skill or annotate the case.
5. Keep the honesty notes section. Self-runs without it become indistinguishable from manufactured validation.
