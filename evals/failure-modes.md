# Failure modes

Common ways strategic-risk memos go wrong, with diagnostic cues. Use this with [`checklist.md`](checklist.md) when reviewing output.

## 1. Generic geopolitical essay

**Symptom:** Reads like a magazine background piece. No decision frame, no options, no indicators.
**Cue:** First paragraph is historical context. Last paragraph is "the situation remains complex."
**Fix:** Demand a decision question and a key judgment in the first 100 words.

## 2. Source theater / fabricated citations

**Symptom:** Plausible-looking citations that do not exist or do not say what is implied.
**Cue:** Round numbers without source URLs; phrases like "according to recent reports" with no link; named institutions used as decoration.
**Fix:** Strip unverified citations. Declare `reasoning-only` mode. Lower confidence.

## 3. False certainty

**Symptom:** Definite forecasts ("X will happen by Q3") without evidence basis.
**Cue:** Probability adverbs absent; no confidence statement; no key unknowns section.
**Fix:** Convert claims to scenarios with triggers. Add explicit confidence and unknowns.

## 4. No decision framing

**Symptom:** Analysis is interesting but not actionable.
**Cue:** No decision is named. Audience is not specified.
**Fix:** Force a `Question / Decision / Audience / Time horizon / Evidence mode` block at the top.

## 5. Missing unknowns

**Symptom:** Memo presents a complete-looking picture with no gaps.
**Cue:** The "Unknowns" section is empty, missing, or boilerplate.
**Fix:** Identify at least the top three material unresolved questions, and tie each to a watch indicator.

## 6. Vague watch indicators

**Symptom:** Watch list is "monitor developments closely" or "engage stakeholders."
**Cue:** No observable signal is specified. No trigger is tied to a posture change.
**Fix:** Each indicator should answer: *what would I see, where, that would change the judgment?*

## 7. Missing actor incentives

**Symptom:** Memo treats institutions as monolithic; no analysis of why each actor would do what.
**Cue:** No actor map. Outcomes presented without causal mechanism.
**Fix:** Add an actor incentives and leverage section.

## 8. No options or trade-offs

**Symptom:** Memo describes a problem but does not engage the user's decision space.
**Cue:** No options table. No trade-off language.
**Fix:** Force at least two distinct options with named trade-offs.

## 9. Overconfident forecasting

**Symptom:** Numerical forecasts presented without a basis ("75% probability of X").
**Cue:** Calibration source is not stated; numbers feel decorative.
**Fix:** Convert to qualitative confidence (Low/Moderate/High) tied to evidence quality, unless the agent has actual quantitative input.

## 10. Unsupported sanctions / legal / regulatory conclusions

**Symptom:** Memo states a legal or sanctions conclusion as fact.
**Cue:** Phrases like "this is a violation" or "this is permitted" without legal citation.
**Fix:** Reframe as risk assessment. Recommend counsel review for any conclusion that requires it.

## 11. Recency confusion

**Symptom:** Memo treats stale information as current; or assumes live verification when none was performed.
**Cue:** No `EVIDENCE ACCESS LIMITED` notice in environments without browsing; references to "today" or "this week" without date anchors.
**Fix:** Anchor in the agent's actual evidence base. Disclose the limit.

## 12. Compression failure

**Symptom:** Useful judgment is buried under decoration.
**Cue:** Executive takeaway repeats the question instead of answering it.
**Fix:** Cut the first third. The takeaway should stand alone.

---

## When composing with Agenda Intelligence MD

The patterns below are derived from real integration runs (see [`docs/integrations/agenda-intelligence-md-live-demo.md`](../docs/integrations/agenda-intelligence-md-live-demo.md)). They are specific to the GTTA + Agenda Intelligence MD composition.

## 13. Score gaming via stripped unsupported claims

**Symptom:** An evidence pack is constructed only from the claims that have sources, hiding the assessments behind the memo's judgment.
**Cue:** `unsupported_claims=0` and `required_but_missing_sources=0` despite the memo containing analytical leaps.
**Why it matters:** The score will look better, but the composition is now misleading. The whole point is that honest gaps lower the score.
**Fix:** Treat the evidence pack as an audit of the *whole* memo, not a curated subset. Every assessment that is not source-backed belongs in `unsupported_claims`.

## 14. JSON projection that drops load-bearing memo content

**Symptom:** The projection (`agenda-brief.json`) passes `validate-brief` and scores well, but the operationally important parts of the memo (options, trade-offs, actor-incentive detail, "what would change the judgment") were not projected.
**Cue:** `validate-brief: OK` and a high `score`, but a reviewer reading only the JSON would not be able to make the decision the memo informs.
**Fix:** Treat the JSON projection as a structural surface for validators, not as the memo. Always preserve the markdown memo as the canonical artifact and ensure the projection links back to it.

## 15. Mode mismatch on raw markdown scoring

**Symptom:** Running `agenda-intelligence score` on a GTTA memo file produces an error like `Not a before/after example: missing ['## Before: generic agent output', '## After: with Agenda-Intelligence.md']`, and a contributor concludes the integration is broken.
**Cue:** The error names specific section headers the file lacks.
**Fix:** Use the JSON projection path. The markdown scorer is shaped for Agenda Intelligence MD's `before/after` example format, not for GTTA memos. This is current behavior; verify against `agenda-intelligence --help` for newer versions.

## 16. `live_source_backed` claim without an evidence pack

**Symptom:** The memo or brief declares `evidence_mode: live_source_backed`, but no evidence pack accompanies it. The structural-only score still looks high (real-run example: 95/100).
**Cue:** A high score with no `--evidence` flag in the scoring command.
**Fix:** If the brief is `live_source_backed`, attach an evidence pack and re-score. Treat brief-only scores as a smoke test, not as a quality grade.

## 17. Stale `retrieved_at` masquerading as current

**Symptom:** Sources tagged `freshness: current` in the evidence pack, but `retrieved_at` is weeks or months old.
**Cue:** Mismatch between `retrieved_at` and the current date when the memo is being acted on.
**Fix:** Re-fetch and re-validate. Sanctions designations, regulatory text, and price-sensitive data can change between retrieval and action; the freshness tag is about the source at retrieval time, not at decision time.
