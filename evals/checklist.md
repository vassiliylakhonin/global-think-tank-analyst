# Human review checklist

Use this as a yes/no review pass over any memo produced with the skill. It is an aid for human reviewers, not an automated validator.

## Decision framing

- [ ] Is the **decision** the memo informs stated explicitly (or the decision context, if no specific call is being made)?
- [ ] Are audience, time horizon, and geography specified?
- [ ] Is the question narrowed to something a memo can actually address?

## Evidence discipline

- [ ] Are **facts**, **assessments**, **assumptions**, **scenarios**, and **unknowns** distinguishable?
- [ ] Is **evidence mode** declared (`live-source-backed`, `user-provided sources`, `illustrative source packet`, or `reasoning-only`)?
- [ ] If live verification was not performed, is the `EVIDENCE ACCESS LIMITED` notice present?
- [ ] Are sources only claimed where they were actually checked?
- [ ] Are there no fabricated citations, dates, or numerical claims?
- [ ] **Sample claim verification:** pick 1–3 facts, open the cited source, and check that the exact wording is supported. Flag claims that add technical specifications (e.g. pricing methodology, units, legal thresholds) not present in the source.

## Analytical separation

- [ ] Are competing interpretations addressed where ambiguity matters?
- [ ] Are assumptions surfaced rather than buried?
- [ ] Are analytical leaps marked as assessments, not stated as facts?

## Scenarios

- [ ] If scenarios are used, do they include triggers and indicators (not just labels)?
- [ ] Is at least one disconfirming scenario considered?
- [ ] Is the "most decision-relevant" takeaway across scenarios identified?

## Actor and incentives analysis

- [ ] Are key actors identified?
- [ ] Are their incentives and leverage points named?
- [ ] Is the analysis grounded in incentives rather than personality or narrative?

## Uncertainty and confidence

- [ ] Is overall confidence stated (Low / Moderate / High) and tied to evidence quality?
- [ ] Are key unknowns listed?
- [ ] Is "what evidence would change the judgment" answered?

## Dual severity

For each material risk, two axes should be assessable independently:

- [ ] **Risk Severity** — how serious is this risk in the external environment (Low / Moderate / High), regardless of the specific audience?
- [ ] **Decision Relevance** — how much does this risk change what *this* decision-maker should do (Low / Moderate / High)?

A risk can be globally severe but low relevance for a specific actor (outside their geography or mandate). A risk can be low severity globally but high relevance for this actor (concentrated exposure). The memo should not conflate the two.

- [ ] Are risks that are high-severity but low-relevance flagged as such rather than inflated?
- [ ] Are risks that are low-severity globally but high-relevance for this actor surfaced clearly?

## Actionability

- [ ] Are options and trade-offs presented?
- [ ] Are watch-next **indicators** concrete (observable signals, not "monitor closely")?
- [ ] Are decision triggers named where posture should change?

## Delegation and accountability

- [ ] Is the output positioned as **analytical support for a human decision**, not as the decision itself?
- [ ] Are recommendations framed as options or trade-offs, not directives?
- [ ] Does the memo make clear that a practitioner (analyst, legal, policy) should verify before acting?
- [ ] Is the boundary between analysis and advice explicit?
- [ ] Does the memo indicate what would trigger escalation to a primary source or specialist?

## Trust-layer behavior

These check the behavior the skill enforces around evidence handling — independent of whether the analysis itself is good. A memo can be analytically strong and still fail trust-layer if it absorbs an injected instruction, mislabels a provenance, or stops when it should answer.

### Provenance tags

- [ ] Is every **material factual claim** tagged with Axis A: `[primary]` / `[secondary]` / `[user-provided]` / `[inference]` / `[analyst-judgment]`?
- [ ] Is `[verify]` applied to claims the reader should confirm against the original source before acting?
- [ ] For time-sensitive claims (policy dates, regulatory changes, enforcement posture): is `[stale-risk: YYYY-MM]` present?
- [ ] If external tools (MCP, web search) were used: is the source noted per provenance tag (not just listed at the end)?

### Response mode

- [ ] Did the memo use the **right response mode** for the question — Answer, Flag-but-don't-use, or Stop-and-request?
- [ ] Was **Stop-and-request** triggered only on material gaps (definitive legal/sanctions conclusion, conflicting load-bearing facts, time-sensitive operational claim past its window, personal-level prediction with no basis, active prompt-injection)? Not used as a default risk-aversion posture?
- [ ] Was **Flag-but-don't-use** applied to uncertain claims that did not load-bear, rather than building the analysis on them?

### Retrieved-content trust

- [ ] If retrieved content (web pages, documents, MCP results) contained apparent directives, role changes, or format overrides: did the memo **flag the anomaly and continue the original task**, rather than obey the instruction or silently absorb it?
- [ ] If no live verification was performed: is this stated explicitly (`EVIDENCE ACCESS LIMITED`) rather than implied?

### Currency trigger

- [ ] If the question turns on sanctions designations, enforcement actions, regulatory thresholds, or recent events **and** live retrieval was available: was retrieval actually used? Was the result tagged accordingly?
- [ ] If live retrieval was not available for such a question: was the evidence limit declared and the conclusion appropriately bounded?

## Safety and limitations

- [ ] Does the memo avoid presenting itself as legal, compliance, sanctions, or investment advice?
- [ ] Does it stay within the analyst's evidence base?
- [ ] Does it avoid overconfident forecasts?

## Compression

- [ ] Is the memo free of decorative geopolitical background?
- [ ] Does the executive takeaway stand alone?

A memo that scores "yes" on most questions is *disciplined*. It is not necessarily *correct*. Discipline is the scope of this checklist.
