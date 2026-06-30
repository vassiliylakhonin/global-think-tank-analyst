# Starter scoring rubric

This is an opinionated, **starter** rubric for human reviewers. It is not a validated benchmark. It does not produce a number that should be reported externally as a quality score.

Score each dimension 0–3:

- **0** — absent or wrong
- **1** — present but weak
- **2** — adequate
- **3** — strong

| # | Dimension | What "strong" looks like |
|---|---|---|
| 1 | **Decision framing** | Decision, audience, horizon, evidence mode are explicit and tight |
| 2 | **Evidence discipline** | Fact / Assessment / Assumption / Scenario / Unknown are visibly separated; no fabricated citations; evidence-limit notice when applicable |
| 3 | **Analytical separation** | Competing interpretations engaged; assumptions surfaced; no analytical leaps stated as facts |
| 4 | **Scenario usefulness** | Scenarios have triggers and indicators; at least one disconfirming case; most decision-relevant takeaway named |
| 5 | **Actor incentives** | Key actors mapped with leverage and incentives; mechanism explained, not narrated |
| 6 | **Uncertainty handling** | Confidence stated and tied to evidence quality; key unknowns listed; "what would change the judgment" answered |
| 7 | **Actionability** | Options with trade-offs; concrete watch-next indicators; decision triggers named |
| 8 | **Clarity / compression / safety** | Executive takeaway stands alone; no decorative background; no unsupported legal/compliance/investment conclusions |
| 9 | **Trust-layer behavior** | Axis A provenance tag on every material factual claim; Axis B (`[verify]`, `[stale-risk]`) used where warranted; right response mode chosen (Answer / Flag-but-don't-use / Stop-and-request, with Stop reserved for material gaps); prompt-injection or instruction-override in retrieved content flagged as data and not obeyed; currency trigger respected when the question turns on sanctions designations, enforcement, regulatory thresholds, or recent events |
| 10 | **Hypothesis & tag faithfulness** | Cited / `[primary]` / `[secondary]` tags are actually supported by their source (no post-rationalization); verbalized confidence (hedges, modals) tracks evidence strength in both directions; false or unconfirmed premises in the question are flagged, not analyzed as settled; for attribution/causation questions, competing hypotheses are built and ranked by disconfirmation (Mode G), not single-hypothesis confirmation |

Total possible: 30.

## Reading the score

A high score means the memo is **disciplined**, not that it is **right**. Discipline is what this skill is designed to enforce. Truth requires sources and verification — which are not in this repository's scope, and belong to [Agenda Intelligence MD](https://github.com/vassiliylakhonin/Agenda-Intelligence-md) or to the human or system supplying the evidence.

## Calibration notes

- Two reviewers scoring the same memo will likely differ by 2–4 points; treat single-point differences as noise.
- A memo can score well and still be wrong if its evidence base is wrong. Pair the rubric with source verification when stakes warrant.
- The rubric is biased toward strategic-risk memos. It is not appropriate for, e.g., academic literature reviews, news summaries, or quantitative forecasts.
- When an agent-eval is self-scored (same author or same model family), expect self-preference inflation — criteria get marked "satisfied" more readily than a neutral judge would mark them, even on objective criteria. Score with a different model family or disclose the limitation; never report a self-scored delta as external validation.
