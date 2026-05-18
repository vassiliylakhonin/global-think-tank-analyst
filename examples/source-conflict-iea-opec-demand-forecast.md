# Source-conflict surfacing — IEA vs OPEC oil-demand forecast (illustrative)

> **Illustrative source packet.** Evidence mode: `illustrative source packet`. No live verification was performed in this environment; figures below are representative of the kind of disagreement these institutions regularly publish, not snapshots of any specific monthly report. The purpose of this example is to demonstrate how the skill surfaces a load-bearing source conflict rather than silently resolving it. Do not use the specific numbers below for any commercial decision.

**User question:** Our trading desk is sizing H2 2026 length on middle-distillate exposure. IEA and OPEC monthly oil-market reports disagree materially on global demand growth for the period. How should we treat that disagreement in the position-sizing decision?

```text
Question: H2 2026 oil-demand-growth uncertainty driven by IEA/OPEC forecast divergence.
Decision: Position sizing on middle-distillate length and hedge ratio for H2 2026.
Audience: Head of oil trading; risk officer.
Time horizon: 6 months.
Evidence mode: illustrative source packet.
Confidence: Moderate, conditional on the conflict being surfaced rather than collapsed.
```

EVIDENCE ACCESS LIMITED: no live verification performed in this environment. Representative figures below are illustrative.

## Executive takeaway

**Key judgment (Moderate confidence, conditional):** IEA and OPEC publish materially different H2 2026 global oil-demand-growth forecasts. The divergence is load-bearing for sizing: a position calibrated to either number alone carries the regret of being long when the other house is right. Apply **flag-but-don't-use** to the absolute growth figure; size length against the lower of the two cases and structure optionality to participate in the higher case rather than averaging across them.

## Source conflict (load-bearing)

Two reputable, methodologically respectable institutions disagree on the H2 2026 global oil-demand-growth number — a fact the position size depends on.

| Position | Source | Provenance | Representative figure | Stated drivers |
|---|---|---|---|---|
| Lower-growth case | IEA monthly Oil Market Report (illustrative) | `[secondary][verify]` | ~0.7 mbd YoY | Post-pandemic demand moderation; accelerating EV penetration in OECD road fuels; efficiency gains |
| Higher-growth case | OPEC monthly MOMR (illustrative) | `[secondary][verify]` | ~1.4 mbd YoY | Non-OECD industrial activity resilience; petrochemical feedstock pull; aviation recovery beyond OECD |

**Why this is a real conflict, not a methodological artifact:**
- The two institutions publish at similar cadence with overlapping data inputs, and the gap persists across multiple recent monthly reports `[inference]`.
- They are not independent sources: both rely on overlapping country-level submissions, refinery-run data, and shipping-tracker feeds `[analyst-judgment]`. Agreement between IEA and *any one* of the secondary trackers (Kpler, Vortexa, Energy Aspects) would NOT count as independent corroboration, since IEA itself draws on those feeds.
- The drivers each house emphasizes are not mutually exclusive — both could be partially correct. The disagreement is about *weighting*, not about facts in dispute.

**Preferred position for sizing — and why:** The IEA case is preferred as the **sizing anchor**, not because it is more likely correct, but because its regret profile is asymmetric: being short on demand and right costs less than being long on demand and wrong, given current term-structure carry and inventory positioning `[analyst-judgment]`. The OPEC case is treated as a **scenario to participate in via options**, not via outright length.

**What is NOT done:** averaging the two figures into a single point estimate. Averaging would silently resolve the conflict and embed an estimate neither house publishes.

## Facts (consensus across both houses)

- **Fact:** Both IEA and OPEC publish monthly global oil-demand forecasts with regional breakdowns `[secondary]`.
- **Fact:** Both have published divergent H2 forecasts in multiple recent reporting cycles `[inference]`.
- **Fact:** Non-OECD demand share has structurally grown over the past decade; the marginal-barrel-of-growth question is increasingly an emerging-markets question `[secondary]`.

## Assessments (with linguistic faithfulness to confidence)

- **Assessment (Moderate confidence):** The OECD-vs-non-OECD weighting gap appears to explain most of the IEA/OPEC divergence; each house implicitly carries a different view of how quickly OECD road-fuel demand erodes `[inference]`.
- **Assessment (Low–Moderate confidence):** If the gap narrows materially within 2 months, the convergence direction is itself information — convergence toward the lower number would suggest emerging-market industrial signals softened; convergence toward the higher number would suggest OECD road-fuel erosion is slower than IEA models `[analyst-judgment]`.
- **Assessment (Moderate confidence):** A position sized to the midpoint of the two forecasts would likely be the worst of both worlds — exposed to the downside if IEA is right and giving up upside capture if OPEC is right `[analyst-judgment]`.

## Scenarios (6 months)

1. **IEA path realizes (lower growth) (treated as the sizing anchor).** Inventory builds through Q3; middle-distillate crack compression in late Q4. **Indicators:** OECD road-fuel demand weakening in monthly EIA/IEA data; refinery-margin compression in NW Europe and US Gulf.
2. **OPEC path realizes (higher growth).** Non-OECD industrial pull surprises to the upside; middle-distillate cracks support through year-end. **Indicators:** China industrial activity prints firm; jet-fuel demand strength in Asia-Pacific.
3. **Convergence to a single revised view within 2 months.** Convergence direction would itself reset position. **Indicators:** Consecutive monthly reports showing the gap narrowing in one direction.
4. **Persistent disagreement through H2.** Position sizing must remain conflict-aware throughout the period; no single number ever becomes "the" forecast. **Indicators:** Gap remains wide; both houses publish unchanged drivers.

## Options and trade-offs

| Option | Pros | Cons |
|---|---|---|
| Size to IEA case; buy upside calls for OPEC case | Asymmetric regret profile; explicit cost of optionality | Option premium drag if neither extreme realizes |
| Size to OPEC case; buy downside puts for IEA case | Captures upside; protected downside | Outright length carry is expensive given term structure |
| Size to midpoint of two forecasts | Simplest implementation | Silently resolves the conflict; worst-of-both regret profile |
| Stay flat until convergence | Zero conflict risk | Forgoes both directions; opportunity cost if disagreement persists |

## Decision-relevant takeaway

The conflict between IEA and OPEC on H2 2026 demand growth is the dominant uncertainty in this sizing decision. Surface it in the trade memo explicitly; do not embed an averaged or undisclosed point estimate. Anchor sizing to the IEA case for regret-asymmetry reasons, with optionality on the OPEC case. Re-evaluate position monthly as each new IEA/OPEC report either narrows or widens the gap.

## Watch-next indicators

- IEA monthly OMR and OPEC monthly MOMR releases (cadence: monthly, mid-month).
- Gap direction: narrowing toward IEA vs narrowing toward OPEC vs persistent.
- EIA STEO as a third, partially-independent reference point (note: also not fully independent of upstream data feeds).
- China industrial production, PMI, and refinery throughput prints (drivers of the OPEC case).
- OECD road-fuel demand series (drivers of the IEA case).

## Confidence and key unknowns

- **Confidence: Moderate**, conditional on the methodology above — the conflict being surfaced rather than collapsed. If a desk silently picked either number as "the" forecast, confidence in the resulting position would be low, regardless of which house was eventually right.
- **Key unknowns:** which house's weighting of OECD-vs-non-OECD drivers will prove closer to realized data; whether the disagreement narrows or persists; whether a third-party tracker provides genuinely independent corroboration of one side.

## What would change the judgment

- Convergence of the two forecasts within 2 months (collapses scenario 1 vs 2 weight; resets sizing).
- A genuinely independent demand series (e.g., a real-time corroborator with non-overlapping inputs) aligning with one house and not the other.
- A regime change in term structure or inventory positioning that alters the regret-asymmetry calculus underlying the IEA anchor.

## Why this example exists

This memo demonstrates the **source-conflict-surfacing rule** from `AGENTS.md` and `SKILL.md`:

- Two materially conflicting sources on a load-bearing fact are NOT silently averaged or one-side-resolved.
- Both positions are named, tagged, and shown with their stated drivers.
- A preferred position is stated **with the reason** (regret asymmetry), not as "we picked IEA because IEA".
- Source independence is explicitly assessed — IEA and OPEC are NOT independent; nor would adding a tracker that re-uses the same upstream data feeds count as independent corroboration.
- The conflict is carried through to the decision (option B+D framing) instead of being collapsed at the takeaway.

## Limitations

Illustrative. Figures are representative, not retrieved. Not investment, trading, or risk-management advice. A real position-sizing decision requires current IEA/OPEC publications, a desk-level term-structure model, and live inventory and positioning data.
