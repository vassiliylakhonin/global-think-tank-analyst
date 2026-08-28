# Supply-chain sanctions exposure — user-provided vendor and counterparty documentation

**Question:** What sanctions exposure does our supply chain carry, and where are the concentrated risks?
**Decision:** Whether to maintain, restructure, or add compliance controls to specific vendor relationships, payment rails, or geographic supply-chain nodes.
**Audience:** Corporate sanctions compliance, procurement, and supply-chain risk teams.
**Time horizon:** 12–18 months, with immediate action on any SDN-adjacent finding.
**Evidence mode:** `user-provided sources`.
**How to use this template:** Replace all `[USER INPUT REQUIRED]` fields with your actual documentation. The skill works from the documents you provide. Do not leave fields blank — without your documents, the analysis is structural only and cannot assess your specific exposure.
**Limitation note:** This is a decision-support template. It is not legal advice, sanctions screening, AML transaction monitoring, or a compliance determination. Operational sanctions decisions require qualified legal and compliance counsel, primary OFAC/EU/UK list checks current as of each transaction, and entity-level KYC. This template structures the analytical questions; it does not answer them without your documents.

---

## Document inputs — paste or attach before analysis

| Document | What to provide | Why it matters |
|---|---|---|
| **Vendor / supplier register** | `[USER INPUT REQUIRED]` — paste or summarise: vendor name, country of incorporation, country of operations, product or service supplied, annual spend, and any known parent or UBO | Identifies the entity population to screen and the concentration of spend by jurisdiction. Without this, exposure assessment cannot be specific. |
| **Payment rail documentation** | `[USER INPUT REQUIRED]` — list the currencies, correspondent banks, and payment channels used for each major vendor or jurisdiction | USD payments route through New York correspondent banks regardless of the transaction's originating jurisdiction. If any leg of a USD payment involves a blocked person, the transaction is blocked. Non-USD payments are not exempt from sanctions rules but carry lower correspondent-banking risk. |
| **Contract terms for high-risk vendors** | `[USER INPUT REQUIRED]` — paste relevant clauses: pricing, delivery jurisdiction, title transfer location, inspection rights, beneficial-ownership representations | Title transfer location, delivery jurisdiction, and inspection rights determine where you take legal and regulatory possession. Beneficial-ownership representations (or their absence) determine what due-diligence defence is available if a counterparty is later found to be sanctions-adjacent. |
| **Existing KYC / due-diligence documentation** | `[USER INPUT REQUIRED]` — paste whatever KYC has been completed: beneficial ownership to UBO, sanctions screening date and list version, PEP screening | Allows the skill to identify gaps in existing coverage rather than repeat what has been done. If screening was done more than 6 months ago or against an old list version, flag it for re-verification. |
| **Product or technology classification** | `[USER INPUT REQUIRED]` — describe what you buy or sell: product category, ECCN (if known), HTS code, dual-use status, end-use | Export-control classification determines whether BIS (EAR), ITAR, or EU dual-use regulation applies — in addition to OFAC sanctions. A product can be legal to buy in the supplying jurisdiction but prohibited to transfer to a third country or end-user. |
| **Geographic footprint of operations** | `[USER INPUT REQUIRED]` — list countries where you have offices, staff, manufacturing, or sales | Determines which sanctions regimes apply to your entity (OFAC jurisdiction over US persons, EU regulation jurisdiction over EU persons, UK OFSI over UK persons) and which regimes require filing or notification. |

---

## Analytical framework — applied once user documents are provided

---

## Bottom line framework

*[Completed once user documents are provided.]*

Supply-chain sanctions exposure concentrates at three points: (1) the entity level — whether any specific vendor or counterparty is SDN-listed or owned/controlled by a blocked person; (2) the payment level — whether any USD payment leg touches a blocked party or blocked property; (3) the product level — whether any product or technology being bought, sold, or transferred is subject to export-control restrictions independent of OFAC sanctions. Jurisdiction labels ("this vendor is in a safe country") do not substitute for entity-level screening.

## Scope and evidence mode

`user-provided sources`. Structural framework is pre-loaded. Specific conclusions require the user-provided documents listed above.

## Sanctions regime map — applicable to most global supply chains

| Regime | Primary list | Applies to | Key trigger |
|---|---|---|---|
| **OFAC SDN and Blocked Persons** | SDN list (https://ofac.treasury.gov/specially-designated-nationals-and-blocked-persons-list-sdn-human-readable-lists) | US persons; any USD transaction | Any transaction with a listed party or their property |
| **OFAC CAATSA secondary sanctions** | Sector-level blocking | Non-US persons dealing with Russian defense/intelligence | 33% or more significant transaction with listed sector entities |
| **EU Consolidated Sanctions List** | EU consolidated list | EU persons and entities incorporated under EU law | Any transaction with a listed party |
| **UK OFSI Consolidated List** | UK sanctions list (https://www.gov.uk/government/publications/the-uk-sanctions-list) | UK persons and entities incorporated under UK law | Any transaction with a listed party |
| **US BIS Entity List / EAR** | BIS Entity List (https://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern) | Any person or entity selling US-origin items or items with US content above de minimis | Export, re-export, or transfer to listed parties without license |
| **UN Security Council sanctions** | UN consolidated list (https://www.un.org/securitycouncil/sanctions/information) | UN member state obligations | Varies by committee and resolution |

## Risk concentration framework — applied to your vendor register

Once the user provides the vendor register, the skill maps exposure using this framework:

### Tier 1 — Immediate screen required

Vendors in any of the following categories warrant SDN-list, EU, and UK sanctions list screening at onboarding and on each material transaction:
- Vendors domiciled in or with operations in Iran, Russia, North Korea, Cuba, Syria, Belarus (fully embargoed or comprehensively sanctioned jurisdictions under OFAC/EU/UK).
- Vendors with beneficial owners who are nationals of comprehensively sanctioned states.
- Vendors in free-zone jurisdictions with opaque beneficial ownership (UAE, Singapore, Hong Kong free zones as re-export or layering risks).
- Vendors supplying dual-use products or technology with known re-export risk to embargoed end-users.

### Tier 2 — Enhanced due diligence

Vendors in the following categories warrant enhanced KYC and periodic re-screening:
- Vendors in jurisdictions on FATF grey list (check current list: https://www.fatf-gafi.org/en/publications/High-risk-and-other-monitored-jurisdictions/).
- Vendors in jurisdictions subject to partial or sectoral sanctions (China technology sector under E.O. 13873 / CHIPS Act restrictions; Russian energy sector; etc.).
- Vendors with parent companies or ultimate beneficial owners in Tier 1 jurisdictions.
- Vendors with USD payment rails through correspondent banks in high-risk jurisdictions.

### Tier 3 — Standard compliance

Vendors in low-risk jurisdictions with transparent beneficial ownership, no dual-use product classification, and established KYC. Standard SDN-list check at onboarding; periodic re-screen (annually or on contract renewal).

## Payment rail analysis framework

*[Applied once payment documentation is provided.]*

Key questions the skill works through:

1. **USD exposure:** Which vendors require USD payment? For each, which bank processes the USD leg? Any USD correspondent bank leg that touches a blocked party will be flagged by the correspondent bank — but the compliance obligation is yours, not the bank's.

2. **Non-USD exposure:** Even non-USD payments can violate sanctions if the transaction itself involves blocked property (e.g., purchasing goods from an SDN-listed vendor in euros does not cure the sanctions violation).

3. **Third-party payment risk:** Are payments made to the vendor directly, or through an intermediary (agent, trading house, distributor)? Intermediary layers obscure the ultimate beneficial recipient and create "willful blindness" risk if the intermediary is later found to be blocked.

4. **Correspondent bank de-risking:** Have any of your payment banks de-risked specific correspondent routes without explaining why? Bank de-risking of a specific corridor or counterparty is a signal that the bank's compliance system flagged something; investigate before assuming the route is clean.

## Export-control overlay

*[Applied once product classification is provided.]*

Sanctions and export controls are parallel regimes; clearing one does not clear the other.

Questions the skill works through:
- Does the product have an ECCN classification, or is it EAR99? (EAR99 is lower risk but not no-risk.)
- Does the product contain US-origin components above de minimis (generally 25% by value; 10% for certain countries)? If yes, US re-export rules apply regardless of where the product is manufactured.
- Does the product appear on the EU dual-use list (EC Regulation 2021/821)? If yes, EU export-control authorisation requirements apply.
- What is the end-use and end-user? A civilian-stated end-use for a dual-use product to an entity on a government procurement list in a high-risk jurisdiction is an elevated risk regardless of product classification.

## Role-based implications

**Sanctions compliance team:**
- Work through the vendor register against the tier framework. Priority: Tier 1 vendors first.
- For any vendor without a documented UBO, flag for enhanced KYC before next contract renewal. Beneficial ownership gaps are an aggravating factor in OFAC enforcement.
- Establish a sanctions clause in all vendor contracts: representations on sanctions status, right to terminate if vendor is designated, and beneficial-ownership certification.
- Set a re-screening calendar: SDN list re-check at minimum annually for Tier 3; quarterly for Tier 2; on each material transaction for Tier 1.

**Procurement team:**
- Any new vendor in Tier 1 jurisdictions requires compliance sign-off before contract execution — not after.
- Payment terms that route through opaque intermediaries should be renegotiated to direct payment or through a named and screened intermediary.
- If a vendor cannot provide UBO documentation, that is a compliance red flag, not a negotiating inconvenience.

**Supply-chain risk team:**
- Geographic concentration in sanctioned-adjacent jurisdictions is a supply-chain resilience risk as well as a compliance risk. Develop alternative sourcing for any single-source supplier in Tier 1 jurisdictions.
- Free-zone concentration risk: if more than 20% of supply-chain spend routes through free-zone entities with opaque UBO, that is a concentration worth addressing structurally.

## Trigger points

| Indicator | Source | Posture change |
|---|---|---|
| Any vendor appears on an updated OFAC SDN or blocked-entity list | OFAC list updates (https://home.treasury.gov/news/press-releases) and real-time screening services | Immediate: stop all payments; freeze pending transactions; legal review; voluntary disclosure assessment |
| FATF grey-lists a jurisdiction where a Tier 2 vendor is domiciled | FATF plenary press releases | Escalate vendor to Tier 1 enhanced screening |
| Correspondent bank returns a payment without explanation or flags a transaction | Internal payment operations | Investigate before re-submitting; de-risking flag by a bank is a compliance signal |
| Vendor requests unusual payment routing (new bank, new beneficiary, third-party payment) | Vendor correspondence | Treat as a red flag; do not proceed without explanation and verification |
| New OFAC general license or advisory naming your industry or product type | OFAC advisories (https://ofac.treasury.gov/recent-actions) | Read carefully; licenses and advisories narrow or expand permissible activity |

## Unknowns — filled from user documents

*[Standard pre-document unknowns:]*
- Beneficial ownership of specific vendors to UBO level
- Whether any vendor's UBO is a national or resident of a comprehensively sanctioned state
- Whether any product in the supply chain is ECCN-classified above EAR99
- Current SDN list status for all vendors (requires live screen)
- Whether any USD payment leg processes through a correspondent bank in an elevated-risk jurisdiction

## Confidence framework

*[Assessed once user documents are provided.]*

- `Verified`: current SDN list status (from live screen); confirmed UBO identity from corporate registry
- `Plausible`: beneficial ownership inference from available public records; risk tier assignment based on jurisdiction and product
- `Judgment`: assessment of whether a specific pattern constitutes "willful blindness" in OFAC's enforcement lens
- `Unknown`: any UBO layer that cannot be confirmed through available documentation

## What would change the judgment

| Evidence update | Direction |
|---|---|
| Vendor provides certified UBO documentation showing no blocked-person nexus | Reduces entity-level risk; does not remove requirement for periodic re-screen |
| UBO documentation reveals a national or resident of a comprehensively sanctioned state | Escalates to immediate legal review; likely requires contract termination |
| Product reclassification shows ECCN above EAR99 | Activates export-control license requirements; separate BIS filing obligation |
| OFAC issues a specific advisory naming your product category or supply chain | Read the advisory; it may expand or narrow permissible activity relative to the current baseline |

## Limitation note

This is a `user-provided sources` decision-support template. It structures the analytical questions; it does not substitute for:
- primary OFAC, EU, and UK sanctions list screening current as of each transaction;
- qualified legal and compliance counsel familiar with your entity's jurisdiction, supply chain, and product classification;
- BIS export-control counsel if dual-use products are in scope;
- entity-level KYC to beneficial ownership.

A "clean" structural analysis from this template does not constitute a compliance clearance. Operational sanctions compliance requires live list screening, qualified review, and documented due diligence.
