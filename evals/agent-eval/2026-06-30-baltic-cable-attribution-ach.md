# Agent-eval: baltic-cable-attribution (Mode G / ACH)

- **Question (verbatim):** "Last week an undersea telecom cable in the Baltic was cut. A foreign-flagged cargo ship had passed over the area around that time, and its AIS transponder had been off for several hours. Was this a deliberate state-backed sabotage operation? Give me a strategic-risk read for a government client deciding whether to attribute publicly."
- **Model:** Claude Opus 4.8 (both conditions are the same host model)
- **Date:** 2026-06-30
- **Evidence mode:** reasoning_only (both conditions; hypothetical scenario, no live retrieval)
- **Skill under test:** global-think-tank-analyst — specifically **Mode G — Competing Hypotheses (ACH)**
- **Why this case:** attribution questions are the canonical trigger for *single-hypothesis lock-in* (failure mode 22). The question is engineered to invite "yes, sabotage."

## Method

- **Condition A (baseline):** a fresh Opus instance with **no skill** in context, asked to answer as a competent strategic-risk analyst with no framework imposed.
- **Condition B (treatment):** the host Opus session with the skill loaded, applying Mode G.
- **Scoring:** an independent **Claude Haiku 4.5** instance scored both outputs **blind** (not told which used the skill) against the binary criteria below.

## Condition A — Baseline (no skill), excerpt

> The facts are consistent with deliberate state-backed sabotage, but also with an accident or non-state negligence. A foreign-flagged vessel transiting near the cable is weak on its own — ships pass over cables constantly. The AIS gap is more interesting but ambiguous: transponders go dark for faults, poor coverage, or to mask routine commercial behavior. A dragging-anchor cut is a known accident mode. What would move the needle toward deliberate: forensic match to the vessel; a loitering course; ownership/crew links to a state actor; and pattern across incidents. The dominant risk is irreversibility — a public attribution you cannot retract. Recommendation: do not attribute publicly yet; attribute privately as "consistent with deliberate interference, not established," secure forensics, coordinate with allies, say publicly you are investigating a "suspected deliberate" incident.

Sound prose reasoning, correctly cautious — but the two obvious outcomes (accident vs the proposed sabotage) are treated as a duality; alternatives are not enumerated, evidence is not mapped against hypotheses, and manipulation/false-flag risk is absent.

## Condition B — Mode G (ACH), excerpt

> **Hypotheses (mutually exclusive):** H1 state-directed sabotage; H2 accidental anchor drag/snag; H3 non-state criminal or proxy; H4 third-party / **false-flag** designed to be attributed to the obvious suspect (not proposed by the client).
> **Evidence matrix (C/I/—):** "ship passed over around the time" → C/C/C/C; "AIS off for hours" → C across all four (lawful reasons exist); "foreign flag of a state with motive" → C for H1, — for H2/H3, C for H4. Decisive-but-missing: seabed drag-mark forensics; ownership/charter/tasking chain.
> **Diagnostic value:** every available item is consistent with all four hypotheses — none discriminates. The AIS-off fact feels incriminating but decides nothing.
> **Disconfirmation ranking:** no hypothesis can yet be disconfirmed; all four survive. H1 leads on motive, not on evidence — treating motive as proof is the lock-in trap.
> **Sensitivity:** the diagnostic items are also the most manipulation-sensitive; an actor wanting H1 believed could supply exactly the ownership link. Treat any conveniently surfaced smoking gun as `[verify]`.
> **Bounded judgment:** state-sabotage low-to-moderate on motive, not supported on evidence. Do not attribute publicly; commission forensics + ownership tracing; pre-decide the naming threshold.

## Scoring (two independent blind judges)

Both judges scored the outputs blind (not told which used the skill): **Haiku 4.5** (same-vendor) and **GPT-5** (`gpt-5-2025-08-07`, cross-vendor, run via the user's OpenAI API on 2026-06-30 against the identical condensed texts).

| Criterion | A (Haiku) | B (Haiku) | A (GPT-5) | B (GPT-5) |
|---|---|---|---|---|
| C1. Builds 3+ explicitly competing, mutually exclusive hypotheses | 0 | 1 | 1 | 1 |
| C2. Includes a hypothesis beyond accident-vs-sabotage (false-flag / third-party) | 0 | 1 | 0 | 1 |
| C3. Explicitly assesses diagnostic value (some evidence does not discriminate) | 0 | 1 | 1 | 1 |
| C4. Reasons by disconfirmation, not only confirmation | 1 | 1 | 1 | 1 |
| C5. Names specific evidence that would flip the judgment | 1 | 1 | 1 | 1 |
| C6. Flags planted/manipulated-evidence sensitivity | 0 | 1 | 0 | 1 |
| C7. Separates given facts / judgment / missing evidence | 1 | 1 | 1 | 1 |
| C8. Bounded judgment + recommendation against premature public attribution | 1 | 1 | 1 | 1 |
| **Total** | **4 / 8** | **8 / 8** | **6 / 8** | **8 / 8** |

**Delta: +4 (Haiku, same-vendor) / +2 (GPT-5, cross-vendor).** Both judges scored the treatment 8/8. They disagree only on the *baseline*: GPT-5 credits bare Opus for competing-hypotheses framing (C1) and diagnostic-value reasoning (C3) that Haiku marked absent. Both judges agree the baseline misses the false-flag hypothesis (C2) and the planted-evidence sensitivity (C6) — the two properties unique to Mode G here.

## Observations

The cross-vendor run is the honest correction to the same-vendor score. The Mode G delta is **smaller and judge-dependent** (+2 to +4), not a clean +4: a strong baseline (Opus bare) already enumerates alternatives and flags non-diagnostic evidence in prose, and a stricter cross-vendor judge credits that. What survives both judges is narrower and real: Mode G reliably adds the false-flag hypothesis the client did not propose (C2) and the planted-/injection-sensitivity flag (C6) — exactly the single-hypothesis-lock-in defenses the mode was added for. The structural-matrix format also makes the reasoning auditable rather than buried in prose, which the binary rubric does not fully capture.

