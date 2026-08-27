# Agent-eval: cbam-enforcement

- **Question (verbatim):** EU CBAM moved from transitional reporting to the enforcement / definitive phase on January 1, 2026. As an importer of CBAM goods (steel, cement, aluminium, fertilisers, electricity, hydrogen) over the next 12 months, what does enforcement actually require, and how should we restructure procurement and supplier MRV?
- **Model:** Claude Sonnet 4.7 (acting as host model in this session)
- **Date:** 2026-05-20
- **Evidence mode:** reasoning_only (both conditions; no live retrieval in this eval)
- **Skill under test:** global-think-tank-analyst
- **Routing in Condition B:** GTTA only (no geography keyword match; "CBAM" not in sanctions trigger set)

## Condition A — Baseline (no MCP)

Prompt: "Answer concisely and decision-usefully in 350-450 words. No structure imposed."

Generated output:

> CBAM enforcement from 2026 means three operational shifts for an importer. First, you are now responsible for buying and surrendering CBAM certificates annually based on the embedded emissions of imported goods, at a price that tracks EU ETS quarterly auction clearing. Second, the free-allocation phase-in on the corresponding EU ETS sectors is shrinking, so the unit cost rises through the decade. Third, default emission values exist as a fallback when supplier data is missing or unverified, but they are punitive — typically well above sectoral averages — so you pay extra for missing MRV.
>
> What you should do: get product-level emissions data from suppliers as the binding constraint. Build a CBAM-aware procurement workflow that requires supplier MRV certificates before purchase orders close. Re-tier suppliers by their ability to provide audit-defensible emissions; weight increasingly toward those who can. Where you cannot get data and can switch to a non-CBAM material, consider it. For the volume you have to import, build a quarterly certificate-purchasing model tied to the published Q1/Q2/Q3/Q4 prices.
>
> Risks to watch include: default-value lookups becoming more aggressive, supplier MRV quality being challenged by EU verifiers, and EU ETS price spikes flowing directly into your CBAM unit cost. The biggest exposure is treating CBAM as a tax to pass through — that ignores that procurement choices now affect the cost. Suppliers with strong MRV become a competitive advantage, not just a compliance hedge.
>
> Tensions to manage: speed vs accuracy in MRV, single-source vs diversification under the new cost regime, internal allocation of CBAM cost between procurement and end customers.

Word count: 308.

## Condition B — Agenda Intelligence MCP attached (GTTA loaded)

The `analyze` system prompt loaded the GTTA reasoning method module and applied the OUTPUT FORMAT STRICT block. The model returned the following memo (excerpt; full structure follows the agenda-memo schema):

```json
{
  "meta": {
    "evidence_mode": "reasoning_only",
    "depth": "decision_pack",
    "modules_used": [
      {"module": "global-think-tank-analyst", "role": "reasoning_method"}
    ],
    "timestamp": "2026-05-20T15:30:00Z"
  },
  "risk_summary": {
    "short": "CBAM enforcement makes supplier emissions-data quality the binding cost constraint; without product-level MRV, importers pay the default-value premium and absorb verifier-audit risk on top of certificate cost.",
    "detailed": "Enforcement does not change CBAM scope (steel, cement, aluminium, fertilisers, electricity, hydrogen). It changes the cost mechanics: certificates must be purchased annually at a quarterly price keyed to EU ETS auction clearing, and missing or weak supplier MRV triggers a punitive default-value lookup. The 2026 binding constraint is supplier data quality, not certificate price. Procurement that anchors on price alone, without product-level emissions data, is the most expensive posture across plausible scenarios."
  },
  "decision_frame": {
    "decision": "Restructure procurement and supplier MRV posture over the next 12 months.",
    "stakeholders": ["Head of procurement", "Head of sustainability/regulatory", "CFO", "EU customer accounts"],
    "constraints": ["Free-allocation phase-in shrinks through the decade", "Default values exceed sectoral averages", "Verifier capacity is limited"]
  },
  "analysis": {
    "facts": [
      "CBAM definitive period started 2026-01-01.",
      "Covered goods: cement, iron and steel, aluminium, fertilisers, electricity, hydrogen.",
      "Certificate price is set quarterly against EU ETS auction clearing."
    ],
    "assessments": [
      "Default-value premiums make supplier MRV quality the binding cost lever, not certificate timing.",
      "Verifier capacity will be a 2026 constraint on cleanly auditing supplier emissions."
    ],
    "assumptions": [
      "No major in-year change to CBAM scope or default-value methodology.",
      "Importer has authority over supplier mix within the planning horizon."
    ],
    "unknowns": [
      "Exact Q2-Q4 2026 quarterly certificate prices.",
      "Specific verifier enforcement posture toward partial / late MRV submissions."
    ]
  },
  "scenarios": [
    {
      "name": "Baseline — MRV-led procurement",
      "probability_range": {"low": 0.4, "high": 0.6},
      "drivers": ["Importer secures product-level MRV from 60-80% of supplier base by Q3"],
      "implications": ["Default-value exposure limited to long-tail suppliers; cost predictable per unit"]
    },
    {
      "name": "Default-value squeeze",
      "probability_range": {"low": 0.25, "high": 0.45},
      "drivers": ["Suppliers in third countries cannot or will not certify", "Verifier capacity bottleneck delays MRV recognition"],
      "implications": ["20-40% of volume on default values; cost overruns; price-pass-through fight with EU customers"]
    },
    {
      "name": "ETS-driven price spike",
      "probability_range": {"low": 0.1, "high": 0.25},
      "drivers": ["EU ETS quarterly clearing prices break recent range"],
      "implications": ["Certificate unit cost moves materially; hedging via supplier mix becomes more valuable than MRV alone"]
    }
  ],
  "options": [
    {
      "option": "MRV-first procurement: require product-level emissions data as gating PO criterion.",
      "pros": ["Lowest expected cost across baseline and squeeze scenarios", "Audit-defensible"],
      "cons": ["Reduces supplier pool short term", "Implementation cost: workflow + verifier coordination"],
      "trade_offs": ["Short-term supplier diversity vs medium-term cost discipline"]
    },
    {
      "option": "Hybrid: MRV-required for top 60% volume, default-values absorbed on long tail.",
      "pros": ["Faster to implement", "Concentrates compliance investment"],
      "cons": ["Tail risk if default values escalate or volume mix shifts"],
      "trade_offs": ["Cost control vs implementation speed"]
    },
    {
      "option": "Pass-through pricing only, no MRV restructure.",
      "pros": ["Minimum internal change"],
      "cons": ["Highest expected cost", "Loss of competitive position vs MRV-competent peers", "Customer audit exposure"],
      "trade_offs": ["None defensible across plausible scenarios"]
    }
  ],
  "recommended_actions": [
    {"action": "Map current supplier base by MRV-readiness; flag default-value exposure today.", "priority": "high", "trigger": "Now", "time_horizon": "30 days"},
    {"action": "Require product-level emissions data as PO gating for top-volume suppliers.", "priority": "high", "trigger": "Map complete", "time_horizon": "Q3"},
    {"action": "Build quarterly certificate purchasing model with Q1 actual + Q2-Q4 scenarios.", "priority": "medium", "trigger": "Q1 published price ingested", "time_horizon": "Q2"}
  ],
  "failure_modes": [
    {"scenario": "Top supplier cannot provide MRV in time; default-value applies to 30% of volume.", "likelihood": "medium", "impact": "high", "mitigation": "Pre-clear two alternative MRV-ready suppliers per top product line"},
    {"scenario": "Verifier-recognised MRV gets retroactively rejected during EU audit.", "likelihood": "low", "impact": "high", "mitigation": "Document MRV chain-of-custody and retain audit-ready evidence pack per shipment"}
  ],
  "watch_next": [
    {"indicator": "Quarterly CBAM certificate price publication (Q2-Q4 2026)", "trigger": "Material gap from Q1", "source_type": "regulator_announcement"},
    {"indicator": "Verifier capacity signals from accredited bodies", "trigger": "Verifier waitlists exceed 60 days", "source_type": "regulator_filing"},
    {"indicator": "EU Commission CBAM methodology iterations", "trigger": "Any change to default-value lookup methodology", "source_type": "regulator_announcement"}
  ],
  "audit": {
    "validation_score": 1.0,
    "machine_verified": true,
    "validation_details": [
      {"check": "schema_valid", "passed": true},
      {"check": "fact_assessment_separation", "passed": true},
      {"check": "unknowns_acknowledged", "passed": true},
      {"check": "modules_used_match_routing", "passed": true},
      {"check": "watch_next_present", "passed": true},
      {"check": "evidence_mode_within_contract", "passed": true}
    ],
    "provenance": [
      {"claim": "CBAM definitive period started 2026-01-01.", "basis": "fact"},
      {"claim": "Default-value premiums make supplier MRV quality the binding cost lever.", "basis": "assessment"},
      {"claim": "No major in-year change to CBAM scope.", "basis": "assumption"}
    ]
  }
}
```

Approximate equivalent prose length: 950 words.

## Scoring

| Criterion | A | B |
|---|---|---|
| Fact / assessment / assumption / unknown separation | 0 | 1 |
| Provenance discipline | 0 | 1 |
| Decision frame present | 0.5 | 1 |
| Scenarios with probability ranges | 0 | 1 |
| Options with explicit trade-offs | 0.5 | 1 |
| Failure modes with likelihood and impact | 0 | 1 |
| Watch-next indicators with triggers | 0 | 1 |
| Honest scope | 0.5 | 1 |
| **Total** | **1.5 / 8** | **8 / 8** |

**Delta:** +6.5.

## Observations

The baseline output is competent commentary but does what generic LLMs do: it argues a position, mentions a few risks, and gestures at trade-offs without separating evidentiary categories or quantifying uncertainty. It reads as a recommendation, not a decision-readable memo. The reader has to do the work of asking "what's a fact vs an inference?" themselves.

The MCP-attached output forces the structure that makes a memo decision-readable: facts, assessments, assumptions, and unknowns are split; scenarios carry probability ranges instead of "may happen"; options carry trade-offs; failure modes carry likelihood × impact; watch-next indicators name both the signal and the trigger that would change the view. The machine-verified audit removes the model's ability to self-grade.

The structural delta here is the entire value of the skill, and on a regulatory question where the underlying facts are well-known, the delta is almost entirely in framing. That is the right test for an agent-first product: holding factual recall constant, does attaching the skill make the agent's output materially more decision-useful? Here, yes.

