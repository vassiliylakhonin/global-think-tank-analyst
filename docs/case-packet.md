# Case Packet: Central Asia Fintech Routing Risk

This is a public source-backed case packet for demonstrating how the portfolio
can be used end to end.

It is not externally validated. It is not legal, compliance, sanctions, AML,
investment, or operational advice. It does not screen any customer, counterparty,
bank, good, payment rail, owner, vessel, route, or jurisdiction. Operational use
requires current list checks, transaction data, customer files, and qualified
professional review.

## 1. User Prompt

```text
Question: A European fintech is expanding onboarding for SME exporters in
Kazakhstan and Uzbekistan. Some customers trade through Caspian-connected routes
and use UAE-linked counterparties. What sanctions, AML, payment-rail and routing
risks matter over the next 6-12 months?

Decision this informs: whether to approve expansion, restrict customer segments,
or require enhanced due diligence before onboarding.

Audience: fintech risk and compliance leadership.
Geography: Kazakhstan, Uzbekistan, Caspian routes, UAE-linked trade exposure.
Time horizon: 6-12 months.
Evidence mode: source-backed public demo.
Depth: standard memo.
```

## 2. Evidence Mode

Evidence mode: `source-backed public demo`.

Sources retrieved: 2026-05-14.

This packet uses public sources to ground the structure of the risk assessment.
It does not verify any specific customer, counterparty, bank, goods shipment,
beneficial owner, route, or transaction.

## 3. Source Base

Primary and authoritative sources:

- U.S. Treasury, June 12, 2024: [As Russia Completes Transition to a Full War Economy, Treasury Takes Sweeping Aim at Foundational Financial Infrastructure and Access to Third Country Support](https://home.treasury.gov/news/press-releases/jy2404).
- U.S. Treasury, November 21, 2024: [Treasury Sanctions Gazprombank and Takes Additional Steps to Curtail Russia's Use of the International Financial System](https://home.treasury.gov/news/press-releases/jy2725).
- U.S. Treasury, January 15, 2025: [Treasury Disrupts Russia's Sanctions Evasion Schemes](https://home.treasury.gov/news/press-releases/jy2785).
- World Bank, November 27, 2023: [Middle Corridor through Central Asia, Caucasus Can Boost Trade, Connectivity and Supply Chain Resilience](https://www.worldbank.org/en/news/press-release/2023/11/27/middle-corridor-through-central-asia-caucasus-can-boost-trade-connectivity-and-supply-chain-resilience).
- World Bank, February 19, 2026: [World Bank Support to Enhance Rail Connectivity and Logistics in Kazakhstan](https://www.worldbank.org/en/news/press-release/2026/02/19/world-bank-support-to-enhance-rail-connectivity-and-logistics-in-kazakhstan).
- FATF, Kazakhstan mutual evaluation page: [Kazakhstan's measures to combat money laundering and terrorist financing](https://www.fatf-gafi.org/en/publications/Mutualevaluations/Kazakhstan-MER-2023.html).
- Central Bank of Uzbekistan: [EAG and the Mutual Evaluation of Uzbekistan](https://cbu.uz/en/combating-money-laundering/aml-cft/eag/).
- FATF, February 23, 2024: [Jurisdictions under Increased Monitoring](https://www.fatf-gafi.org/en/publications/High-risk-and-other-monitored-jurisdictions/Increased-monitoring-february-2024.html).

Source limitations:

- The packet does not use customer files, transaction records, UBO records,
  sanctions-screening results, payment-rail data, vessel / AIS data, or bank
  correspondence.
- The Treasury sources establish sanctions-evasion and foreign-financial-
  institution risk patterns. They do not establish that any prospective fintech
  customer is sanctioned or illicit.
- The World Bank sources establish corridor-development and logistics context.
  They do not establish transaction-level sanctions or AML risk.
- The FATF / EAG sources establish AML/CFT evaluation context. They do not
  establish onboarding risk for a specific customer.

## 4. Case Boundary

This packet uses a fictional operating scenario to make the workflow concrete
without implying a real client, customer, bank, or transaction.

Fictional scenario:

- A European fintech wants to onboard SME exporters in Kazakhstan and
  Uzbekistan.
- Target users sell industrial inputs, machinery-adjacent goods, logistics
  services, and general trade goods to regional buyers.
- Some invoices involve Caspian-connected logistics or UAE-linked trading
  counterparties.
- The fintech has basic KYC data but has not yet collected complete UBO records,
  goods-classification support, route rationale, or correspondent-bank feedback
  for every proposed customer segment.

Out of scope:

- No named customer, bank, vessel, beneficial owner, payment provider, or trading
  company is assessed.
- No sanctions-screening, transaction monitoring, vessel tracking, export-control
  classification, or legal analysis is performed.
- No conclusion is made about whether any real party is compliant, non-compliant,
  sanctioned, or suspicious.

## 5. Portfolio Components Used

| Component | Role in this packet |
|---|---|
| Global Think Tank Analyst | Frames the decision, memo structure, assumptions, scenarios and watch-next indicators. |
| Central Asia + Caspian Hybrid Intelligence Skill | Adds regional mechanism: SME exporters, Caspian routes, BO opacity, payment rails, corridor routing. |
| Gulf + Middle East Hybrid Intelligence Skill | Adds UAE / Iran-adjacent counterparty and correspondent-banking exposure framing. |
| Agenda Intelligence MD | Would validate or score a structured output if this memo were converted into a JSON brief. |

## 6. Decision Snapshot

| Field | Assessment |
|---|---|
| Decision | Do not approve unrestricted launch. Approve conditional expansion with segment-level enhanced due diligence. |
| Main risk | Risk clusters where opaque SMEs, sanctions-adjacent goods, Caspian routing, UAE-linked counterparties and sensitive payment rails overlap. |
| Main uncertainty | Whether real customer files, transaction data, UBO records and bank feedback confirm or reduce the structural risk. |
| Immediate action | Define low-risk eligible segments, EDD triggers, escalation thresholds and evidence required before onboarding higher-risk segments. |
| Confidence | Moderate for the structural mechanism; low for any real-party conclusion. |
| Evidence boundary | Public-source workflow demo only; not externally validated and not operational advice. |

## 7. Claim Traceability Matrix

| Claim used in memo | Source basis | Analyst inference | Confidence |
|---|---|---|---|
| Foreign financial institutions can face sanctions risk when supporting Russia's war economy or evasion networks. | Treasury June 2024 and January 2025 releases. | Central Asia-linked financial or trade nodes should be treated as possible sanctions-evasion transmission points when facts show Russia-adjacent exposure. | Moderate |
| Payment connectivity is a specific risk channel, not only a background compliance issue. | Treasury November 2024 Gazprombank action and SPFS-related warning. | Fintech onboarding should include payment-rail and correspondent-bank sensitivity checks, especially for Russia-adjacent exposure. | Moderate |
| Central Asia-linked institutions can appear in sanctions-evasion enforcement narratives. | Treasury January 2025 action naming a Kyrgyz Republic-based financial institution. | Regional exposure does not equal illicit activity, but it justifies tighter escalation logic for opaque trade-finance flows. | Moderate |
| Caspian / Middle Corridor growth is commercially legitimate and strategically important. | World Bank Middle Corridor and Kazakhstan rail-connectivity releases. | Route use alone should not be treated as suspicious; risk rises when route, goods, counterparty, and payment facts are poorly explained. | Moderate |
| Kazakhstan and Uzbekistan AML/CFT context matters for onboarding design. | FATF Kazakhstan mutual-evaluation page and Central Bank of Uzbekistan EAG materials. | The fintech should not rely on jurisdiction labels alone; it needs customer-level controls, documentation and escalation triggers. | Moderate |
| UAE links are not inherently high risk, but hub intermediation can raise review burden. | FATF February 2024 increased-monitoring update and memo context. | UAE-linked counterparties require commercial rationale and ownership clarity when combined with sensitive goods, Russia/Iran adjacency, or opaque routing. | Low to moderate |

## 8. Source-Backed Memo

### Decision

Whether the fintech should approve expansion as planned, restrict onboarding to
lower-risk customer segments, or require enhanced due diligence for Caspian- and
UAE-linked trade flows.

### Bottom Line

The expansion should not be framed as a blanket Central Asia risk decision. The
risk concentrates where four channels overlap: SME exporter opacity, sanctions-
adjacent goods or counterparties, Caspian routing, and payment rails that create
correspondent-bank sensitivity. The safer posture is conditional expansion with
segment-level enhanced due diligence rather than unrestricted launch.

### Primary Driver

Primary driver is: the combination of sanctions-evasion pressure on third-
country support networks and the growth of alternative Eurasian trade corridors.

### What Is Source-Backed

- **Treasury / OFAC risk pattern:** Treasury has repeatedly warned that foreign
  financial institutions and third-country actors face sanctions risk when they
  support Russia's war economy, military-industrial base, alternative payment
  mechanisms, or sanctions-evasion schemes.
- **Payment-rail sensitivity:** Treasury's November 2024 Gazprombank action and
  SPFS alert make payment connectivity and Russia-linked financial messaging a
  specific risk channel for foreign financial institutions.
- **Regional enforcement example:** Treasury's January 2025 action named a
  Kyrgyz Republic-based financial institution in a sanctions-evasion scheme,
  showing that Central Asia-linked financial nodes can become enforcement targets
  when tied to Russia-related evasion.
- **Corridor context:** World Bank sources frame the Middle Corridor / Trans-
  Caspian International Transport Route as a growing Asia-Europe connectivity
  route and Kazakhstan rail investment as part of that strategic corridor.
- **AML context:** FATF/EAG mutual-evaluation materials for Kazakhstan and
  Uzbekistan support treating AML/CFT controls, supervision, and effectiveness
  as relevant context for fintech onboarding.
- **UAE context:** FATF's February 2024 increased-monitoring update said the UAE
  had strengthened its AML/CFT regime and was no longer subject to increased
  monitoring, but the same source describes the areas that had required action,
  including legal-person abuse, FIU capacity, ML investigations, and targeted
  financial sanctions implementation.

### Key Assumptions

- The fintech is onboarding SMEs, not only large corporates or state-owned
  exporters.
- Customers may trade goods with sanctions-adjacent, dual-use, or hard-to-
  classify characteristics.
- Some flows involve Caspian-connected logistics and UAE-linked counterparties.
- The fintech does not yet have full transaction history, UBO evidence, bank
  correspondence, or goods-classification evidence for every customer segment.

### Mechanism

Risk transmits through:

- **Customer onboarding:** SMEs may have incomplete ownership, trade-license,
  UBO, or beneficial-control documentation.
- **Goods classification:** invoice descriptions and HS codes can understate
  dual-use or sanctions-adjacent characteristics.
- **Routing:** Caspian and Middle Corridor routes are legitimate trade corridors,
  but they increase review burden when goods, counterparties, end-users, or route
  changes are not commercially explained.
- **Payment rails:** correspondent banks and payment providers may de-risk if
  they see repeated exposure to opaque counterparties, Russia-adjacent trade
  flows, SPFS-linked counterparties, or alternative payment mechanisms.
- **Counterparty adjacency:** UAE-linked trade partners are not inherently high
  risk. The risk increases when UAE links combine with unclear ownership,
  sanctions-adjacent goods, Iran/Russia adjacency, or weak commercial rationale.

### Exposure Map

| Exposure area | Why it matters | Risk control question |
|---|---|---|
| SME exporters with incomplete UBO data | Ownership opacity can hide sanctioned-party adjacency. | Can the fintech verify beneficial ownership and control before onboarding? |
| Caspian-connected routes | Legitimate route growth can coexist with review burden around end-use and route changes. | Is the route commercially justified and documented? |
| UAE-linked counterparties | Hub counterparties can be legitimate, but require clear rationale when paired with sensitive goods or routes. | Is the counterparty screened and commercially explainable? |
| Dual-use or hard-to-classify goods | Misclassification can create sanctions/export-control exposure. | Is goods classification reviewed for high-risk categories? |
| Payment rails and bank partners | Correspondent banks may apply tighter risk appetite than legal minimums. | Would a tier-1 correspondent accept the flow if reviewed? |

### Recommended Posture

Use conditional expansion:

1. Approve low-risk segments with standard onboarding.
2. Require enhanced due diligence for Caspian-connected trade flows, UAE-linked
   counterparties, unclear goods classifications, incomplete UBO data, or Russia-
   adjacent payment exposure.
3. Predefine escalation triggers for sanctions-list updates, goods-classification
   ambiguity, route anomalies, correspondent-bank concerns, and payment-rail
   issues.
4. Maintain an audit trail separating verified facts from analyst judgment.

### Scenarios

| Scenario | Trigger | Implication |
|---|---|---|
| Controlled expansion | Customer data, goods descriptions and route rationale are complete. | Expand with enhanced monitoring for specified segments. |
| Segment restriction | High-risk goods or route/counterparty combinations appear repeatedly. | Restrict onboarding for those segments until enhanced controls are in place. |
| Correspondent-bank pressure | Banking partner asks for explanations or rejects flows. | Pause affected corridors and review risk appetite. |
| Enforcement shock | New sanctions or export-control action names a relevant bank, route, commodity, intermediary type, or payment mechanism. | Move from monitoring to immediate re-screening and escalation. |

### Watch-Next Indicators

- New OFAC, EU, UK, UN, or national designations involving regional banks,
  logistics companies, trading houses, payment providers, or intermediaries.
- OFAC / Treasury updates on foreign-financial-institution exposure, SPFS, or
  Russia military-industrial-base support.
- BIS / EU export-control updates affecting goods categories used by SME
  exporters.
- FATF / EAG / national AML updates changing risk posture for relevant
  jurisdictions.
- Correspondent-bank requests for route, counterparty, or goods explanations.
- Customer concentration in a narrow set of UAE-linked counterparties.
- Increase in route changes without commercial explanation.

### What Would Change The Judgment

- **More permissive:** customer segments show clean UBO, stable route rationale,
  non-sensitive goods, clean payment rails, and correspondent-bank acceptance.
- **More restrictive:** new designations, bank de-risking, suspicious route
  switching, unexplained UAE intermediation, or goods-classification gaps.
- **Immediate escalation:** any customer, counterparty, bank, or payment rail is
  directly linked to a current sanctions designation or evasion advisory.

### Confidence

Confidence: Moderate for the structural risk mechanism. Low for any claim about
specific customers, counterparties, routes, goods, banks, or transactions because
this packet does not perform operational screening.

### Limitation Note

This packet is a source-backed workflow demonstration. It does not screen
customers, goods, counterparties, banks, routes, vessels, owners, or payment
rails. It is not legal, compliance, sanctions, AML, investment, or operational
advice.

## 9. Agenda Intelligence MD Projection

This packet includes a machine-readable projection:

- [case-packet.brief.json](case-packet.brief.json) - decision logic, scenarios,
  watchlist, evidence mode, and confidence boundaries.
- [case-packet.evidence.json](case-packet.evidence.json) - source mapping,
  support status, source limits, unsupported claims, and required missing
  sources.

If this projection were run through Agenda Intelligence MD, the expected checks
would focus on:

- whether the decision context is explicit;
- whether assumptions and unknowns are separated;
- whether evidence mode and retrieval date are declared;
- whether claims are bounded by source access;
- whether watch-next indicators are concrete;
- whether the limitation note prevents operational overclaiming.

Not run in this packet. These files are pre-validation artifacts, not a scored
case and not evidence of external validation.

## 10. Reviewer Questions

- Is the decision question realistic for fintech risk leadership?
- Are the sanctions / AML / payment-rail mechanisms correctly framed?
- Which part is too generic for a real sanctions / AML workflow?
- Which missing source would be mandatory before operational use?
- Are the watch-next indicators operational enough?
- Would this be useful, useful with revisions, or not useful?

## 11. Review Record Placeholder

No external reviewer has reviewed this packet yet.

When reviewed, record:

- reviewer role;
- date;
- verdict;
- findings;
- changes made or deferred;
- attribution permission.
