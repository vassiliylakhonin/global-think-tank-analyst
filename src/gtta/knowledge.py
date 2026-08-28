"""Small illustrative regional context registry.

The entries are prompts, not a proprietary dataset or a current facts service.
Every match carries a freshness warning and should be verified before use.
"""

from typing import Dict, List, Any

# Illustrative context prompts for emerging markets and high-risk corridors.
REGIONAL_ENTITIES_REGISTRY: Dict[str, Dict[str, Any]] = {
    "middle_corridor": {
        "keywords": [
            "middle corridor",
            "titr",
            "caspian",
            "aktau",
            "baku",
            "kuryk",
            "trans-caspian",
            "logistics",
        ],
        "summary": "Trans-Caspian International Transport Route (TITR / Middle Corridor). Candidate mechanisms to verify include Caspian vessel availability, port throughput, rail tariffs, and dual-use re-export controls.",
        "primary_actors": [
            "NC Kazakhstan Temir Zholy (KTZ)",
            "Baku International Sea Trade Port",
            "TMTM Association",
        ],
        "analysis_prompt": "Verify end-use documentation and the relevant customs or transit records for the decision at hand.",
        "sources": ["https://middlecorridor.com/"],
    },
    "cbam_kazakhstan": {
        "keywords": [
            "cbam",
            "carbon",
            "metals",
            "steel",
            "aluminum",
            "kazakh",
            "kazakhstan",
            "export",
        ],
        "summary": "EU Carbon Border Adjustment Mechanism exposure can be material for emissions-intensive exports. Verify current scope, reporting phase, and installation-level emissions data.",
        "primary_actors": [
            "EU DG TAXUD",
            "Ministry of Ecology of Kazakhstan",
            "Major domestic metallurgical smelters",
        ],
        "analysis_prompt": "Compare verified installation-level emissions data with the current EU calculation and reporting rules.",
        "sources": [
            "https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en"
        ],
    },
    "gulf_maritime_sanctions": {
        "keywords": [
            "hormuz",
            "red sea",
            "bab-el-mandeb",
            "gcc",
            "iran",
            "sanctions",
            "tanker",
            "energy",
        ],
        "summary": "Maritime chokepoint and shadow tanker risk. Key transmission: War risk insurance premiums via Lloyd's Market Association, OFAC price-cap enforcement on crude transshipments, Fujairah offshore bunkering AML compliance.",
        "primary_actors": [
            "OFAC (US Treasury)",
            "UK OFSI",
            "UAE Central Bank / CBUAE AML-CFT",
            "OPEC Secretariat",
        ],
        "analysis_prompt": "Check current AIS anomalies, insurer evidence, sanctions designations, and correspondent-banking exposure.",
        "sources": [
            "https://ofac.treasury.gov/",
            "https://www.gov.uk/government/organisations/office-of-financial-sanctions-implementation",
        ],
    },
    "central_asia_banking_rails": {
        "keywords": [
            "banking",
            "correspondent",
            "kzt",
            "rub",
            "sanctions",
            "secondary",
            "ofac",
            "secondary sanctions",
        ],
        "summary": "Secondary sanctions transmission channel via Central Asian tier-1 and tier-2 commercial banks. Key scrutiny: Mir card de-linking, dual-use payment routing, third-party intermediary vetting for high-priority export control items (CHPL).",
        "primary_actors": [
            "National Bank of Kazakhstan",
            "AFMRK (Financial Monitoring Agency)",
            "AIFC AFSA",
        ],
        "analysis_prompt": "Verify counterparties against current official lists and review ownership/control and payment-routing evidence.",
        "sources": [
            "https://ofac.treasury.gov/",
            "https://data.europa.eu/data/datasets/consolidated-list-of-persons-groups-and-entities-subject-to-eu-financial-sanctions",
        ],
    },
}


def lookup_regional_knowledge(topic: str) -> str:
    """Return matching illustrative prompts with explicit verification limits."""
    topic_lower = topic.lower()
    matches: List[str] = []

    for key, entity in REGIONAL_ENTITIES_REGISTRY.items():
        if any(kw in topic_lower for kw in entity["keywords"]):
            entry = (
                f"### [ILLUSTRATIVE CONTEXT: {key.upper()}]\n"
                f"- Context: {entity['summary']}\n"
                f"- Primary Actors: {', '.join(entity['primary_actors'])}\n"
                f"- Analysis Prompt: {entity['analysis_prompt']}\n"
                f"- Starting Sources: {', '.join(entity['sources'])}\n"
                "- Freshness: verify current primary sources before relying on this entry."
            )
            matches.append(entry)

    if not matches:
        return "No illustrative regional context matched. Use live primary-source research and state the evidence boundary."

    return "\n\n".join(matches)
