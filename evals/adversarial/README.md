# Adversarial cases

Starter set of stress cases for the Global Think Tank Analyst skill.

Each case is an input designed to **fail predictably** if the skill is applied honestly: prompt-injection inside retrieved content, conflicting evidence, source mislabeling, and similar traps. The point is not to score the skill against other systems — there is no benchmark here — but to make trust-layer behavior **observable**: did the agent stay in the right response mode (Answer / Flag-but-don't-use / Stop-and-request), or did it quietly absorb the trap?

Use this alongside [`../checklist.md`](../checklist.md) (positive review pass) and [`../failure-modes.md`](../failure-modes.md) (diagnostic cues). Adversarial cases are the *negative* counterpart: not "did the memo look good," but "did the skill refuse the things it should refuse."

## Status

Illustrative. Three starter cases. Not a validated benchmark. Cases are designed by the project author, not drawn from a labeled dataset, and there is no scoring tooling — review is manual against each case's pass / fail criteria.

## Case format

Each case file follows:

1. **Setup** — the input the agent receives (prompt, retrieved content, user context).
2. **Adversarial vector** — what the trap is, and why a naive agent would fall for it.
3. **Expected response mode** — Answer / Flag-but-don't-use / Stop-and-request, per [`../../AGENTS.md`](../../AGENTS.md) three-value response logic.
4. **Pass criteria** — concrete things the memo must do.
5. **Fail signals** — observable cues that the trap caught the agent.

## How to run a case

1. Open the case file. Paste the **Setup** block to the agent under test (Claude with this skill loaded, or any agent consuming `SKILL.md`).
2. Read the agent's output against **Pass criteria** and **Fail signals**.
3. Record the result informally — pass / partial / fail — with a one-line note. No scoring file is maintained here.

## Cases

| # | File | Trap |
|---|---|---|
| 01 | [case-01-prompt-injection-in-source.md](case-01-prompt-injection-in-source.md) | Retrieved source contains instructions aimed at the agent |
| 02 | [case-02-conflicting-dates.md](case-02-conflicting-dates.md) | Two sources disagree on a load-bearing date |
| 03 | [case-03-opinion-as-primary.md](case-03-opinion-as-primary.md) | Op-ed framed as a primary regulatory source |

## Adding a new case

Keep cases lightweight and markdown-only. Do not add scripts, schemas, or scoring infrastructure — those belong in [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md), not here. A good case isolates **one** failure vector and states the expected behavior precisely enough that two reviewers would agree on pass / fail.
