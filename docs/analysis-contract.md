# Analysis contract — provenance, calibration, response modes

How a memo produced with this skill must handle claims: how each factual claim is tagged, how decisiveness must track evidence, when to answer versus stop, and how every input claim is accounted for.

The machine-executable subset of this contract is documented in
[`contract-checker.md`](contract-checker.md). Passing that preflight establishes
only observable method shape, not factuality or claim/source support.

`AGENTS.md` states these rules in summary and points here for the detail. This file is the authority on the specifics; the summary never overrides it. Runtime execution behavior is in [`SKILL.md`](../SKILL.md).

## Per-claim provenance tags

Every factual claim in memo output should carry a provenance tag. Two axes — use one from Axis A and optionally one or more from Axis B.

**Axis A — source type (exactly one per claim):**
- `[primary]` — first-hand source: official document, regulatory filing, court record, directly read in this session
- `[secondary]` — third-party analysis, media, research report
- `[user-provided]` — provided by the user in this session, not independently verified
- `[inference]` — derived from other facts in this memo or session
- `[analyst-judgment]` — evaluative judgment, not a factual claim

**Axis B — action flags (optional, added to Axis A tag):**
- `[verify]` — reader should confirm against original source before acting
- `[stale-risk: YYYY-MM]` — last confirmed at that date; may be outdated

Examples:
- "The regulation entered into force in March 2024 [primary][verify]."
- "Analysts widely expect further tightening [secondary]."
- "The political cost of reversal is high [analyst-judgment]."

**Tag faithfulness, not just tag presence:** a provenance tag is honest only if the cited source actually supports the specific claim it is attached to. Attaching a plausible-looking `[primary]` / `[secondary]` tag to a claim the source does not establish — including citations added after the conclusion was already formed (post-rationalization) — is a fabrication, not a formatting nicety. When a source supports only part of a claim, narrow the claim to what the source actually carries rather than over-tagging.

## Linguistic faithfulness

The decisiveness of the language must match the stated confidence and the provenance tag.

- A claim tagged `[analyst-judgment]` or carrying low confidence must not be phrased as a fact. Use hedges: "likely", "appears to", "suggests", "if X holds".
- A claim tagged `[primary]` with high confidence should be stated plainly. Over-hedging a verified fact is also a failure.
- Do not use confident framing ("clearly", "will", "is") for inferences, projections, or scenarios.
- Confidence ranges (e.g. "moderate confidence", "60%") are preferred over implicit decisive tone.

Mismatch between tone and evidence is treated as an honesty-rule violation, not a style issue.

The rule exists because verbalized confidence cannot be trusted by default: measured across models and datasets, LLM confidence statements are largely detached from actual accuracy, and confidence expression is encoded separately from calibration (arXiv:2603.25052). Tying decisiveness to provenance tags and explicit confidence bands is the discipline that substitutes for calibration the model does not have.

This is checkable, not vibes: the hedges and modal verbs in the prose should track the strength of the underlying evidence and its provenance tag. A claim stated more decisively than its evidence supports — or a verified `[primary]` fact buried under needless hedges — is a calibration failure in either direction. When the right level is unclear, state confidence explicitly (a range or a qualitative band) rather than leaning on tone to carry it.

## Three-value response logic

Do not default to binary "answer or refuse." Apply three values:

1. **Answer** — sufficient basis exists; state the analysis.
2. **Flag-but-don't-use** — note the uncertainty as a caveat but do not build analysis on the uncertain claim. State explicitly: "I cannot verify [X]; it is not used in the analysis below."
3. **Stop and request** — basis is insufficient and the gap is material to the conclusion; ask for sources or context before proceeding.

Silence about known doubt is as misleading as a confident assertion.

## Input-claim accounting

When the analysis is built on user-provided sources or a source record with an extracted key-claims table (the Source Ingest skill in Agenda Intelligence MD produces one), the handoff must account for every extracted claim. Each input claim ends in exactly one state:

- **used** — woven into the analysis, carrying its provenance tag;
- **flagged-but-not-used** — stated per three-value response logic: "I cannot verify [X]; it is not used in the analysis below";
- **conflict-surfaced** — contradicts another source or the prior assessment; both positions named with their provenance;
- **out-of-scope** — explicitly excluded, with a one-line reason.

An input claim in none of these states was silently dropped. Silent omission of an input claim is treated the same way as silence about known doubt: an honesty-rule violation, not a style choice. The rule governs accounting, not length — the analysis stays selective, and the accounting is what makes the selection visible. A short "Input claims not used" line near the limitation note satisfies it when several claims share one state.
