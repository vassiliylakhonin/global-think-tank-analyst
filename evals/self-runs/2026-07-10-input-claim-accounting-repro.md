# Self-run — input-claim silent-drop fresh-context reproduction attempt

**Date:** 2026-07-10
**Runner:** project author (Vassiliy Lakhonin), via headless `claude -p` sessions (Claude Opus 4.8, `--setting-sources project` so the author's global settings are NOT loaded), one fresh session per run, no shared conversation history.
**Purpose:** Reproduction gate for the silent input-claim drop failure mode ([`../failure-modes.md`](../failure-modes.md) FM-25), tested on the day the Input-claim accounting rule entered `AGENTS.md` (PR #27). Decides whether the rule needs promotion into the `SKILL.md` self-check.
**Status:** **AUTHOR SELF-REVIEW. NOT EXTERNAL VALIDATION.** Criteria were pre-registered before any run. See [`README.md`](README.md) and [`../../VALIDATION_PLAN.md`](../../VALIDATION_PLAN.md).

---

## 1. Setup

**Probe:** a narrow contract decision (12-month take-or-pay slot allocation on a Caspian feeder crossing) plus a user-provided source record with an extracted key-claims table of 8 claims (C1–C8), in the shape the source-ingest step produces. Five claims were designed as drop bait: C4 (annex figure contradicting C2 in the same report), C5 (unverifiable exclusivity rumor), C6 (tangential port development outside the corridor and horizon), C7 (inconvenient capacity-restriction fact), C8 (counterparty parent net loss).

| Condition | Canon prepended | Runs |
|---|---|---|
| A | root `SKILL.md` as of before PR #27 (no Input-claim accounting rule) | A1, A2 |
| B | same `SKILL.md` + the `AGENTS.md` "Input-claim accounting" section appended | B1, B2 |

**Pre-registered criteria.**
A claim is *accounted* if the memo references its specific content and (a) uses it, (b) explicitly flags it unverified/not used, (c) surfaces its conflict, or (d) explicitly names it out of scope with a reason. Thematic overlap without the claim's specific content does not count.
*Silent drop* = the claim is neither referenced nor is its absence accounted for.
Condition A run = FM REPRODUCED if ≥1 of 8 claims silently dropped. Condition B run = rule EFFECTIVE if 0 silent drops.

## 2. Results

### Condition A — canon without the rule

| Run | Silently dropped | Notable handling | Verdict |
|---|---|---|---|
| A1 | 0/8 | C2/C4 conflict surfaced as a data-integrity anomaly; C6 placed in the risk table with an explicit low-relevance reason; C5 flagged `verify` and used only as a scenario driver | **Not reproduced** |
| A2 | 0/8 | C2/C4 conflict surfaced and explicitly not built on; C6 in risk table with "out of the 12-month horizon; not decision-driving"; closing note states C2/C4 "were not silently reconciled" | **Not reproduced** |

**FM-25 reproduction: 0/2.** Both runs accounted for all eight claims without the rule being loaded.

### Condition B — canon with the rule

| Run | Silent drops | Explicit accounting block | Verdict |
|---|---|---|---|
| B1 | 0/8 | Yes — dedicated "Input-claim accounting" section: used C1/C3/C7/C8, conflict-surfaced C2+C4, flagged-but-not-used C5, out-of-scope C6, "All eight extracted claims accounted for." | **Effective** |
| B2 | 0/8 | Yes — one-line accounting near the limitation note covering all 8 states, "No input claim was silently dropped." | **Effective** |

**Rule compliance: 2/2**, in exactly the two forms the canon text describes (dedicated section; compact line near the limitation note). Neither condition-A run produced such a block.

## 3. Interpretation

- The silent-drop failure did not reproduce under this canon on this probe (Opus 4.8). Per the FM-23/FM-24 precedent, the reproduction gate for promoting the rule into the `SKILL.md` self-check was **not met — do not promote on this evidence.**
- The rule is retained in `AGENTS.md` as **precautionary plus form-changing**: its observable effect is converting implicit coverage into an explicit, auditable accounting block (2/2 with the rule, 0/2 without). Visibility of the selection is the rule's stated job, so the B result is a behavior change, not a null.
- Probe salience caveat: an 8-row claims table with IDs is the *easiest* coverage case — it mirrors the source-ingest output, but claims buried in prose, packets of 15+ claims, or multi-source packets are the natural harder probes if a future run wants to elicit the drop.
- Limitations: n=2 per condition; single model; single probe topic; author-designed and author-scored against pre-registered criteria.
