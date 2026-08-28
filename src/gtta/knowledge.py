"""Proprietary Regional Domain Knowledge & Entity Registry for Global Think Tank Analyst."""

from typing import Dict, List, Any

# Structured domain knowledge base for emerging markets & high-risk corridors
REGIONAL_ENTITIES_REGISTRY: Dict[str, Dict[str, Any]] = {
    "middle_corridor": {
        "keywords": ["middle corridor", "titr", "caspian", "aktau", "baku", "kuryk", "trans-caspian", "logistics"],
        "summary": "Trans-Caspian International Transport Route (TITR / Middle Corridor). Bottlenecks: Caspian vessel availability, Aktau/Kuryk port container throughput, Poti/Batumi rail transit tariffs. Transmission risk: Dual-use re-export controls under EU sanctions packages (11th-14th).",
        "primary_actors": ["NC Kazakhstan Temir Zholy (KTZ)", "Baku International Sea Trade Port", "TMTM Association"],
        "compliance_vector": "Requires verification of transit end-use certificates and tracking through Kazakh/Georgian customs platforms."
    },
    "cbam_kazakhstan": {
        "keywords": ["cbam", "carbon", "metals", "steel", "aluminum", "kazakh", "kazakhstan", "export"],
        "summary": "EU Carbon Border Adjustment Mechanism (CBAM) enforcement phase. Kazakhstan exposure concentrated in basic metals (iron, steel, aluminum). Embedded emissions risk: coal-dominated electricity grid (~70% coal generation).",
        "primary_actors": ["EU DG TAXUD", "Ministry of Ecology of Kazakhstan", "Major domestic metallurgical smelters"],
        "compliance_vector": "Direct reporting of actual installation-level emissions under EU calculation rules vs default penalty values."
    },
    "gulf_maritime_sanctions": {
        "keywords": ["hormuz", "red sea", "bab-el-mandeb", "gcc", "iran", "sanctions", "tanker", "energy"],
        "summary": "Maritime chokepoint and shadow tanker risk. Key transmission: War risk insurance premiums via Lloyd's Market Association, OFAC price-cap enforcement on crude transshipments, Fujairah offshore bunkering AML compliance.",
        "primary_actors": ["OFAC (US Treasury)", "UK OFSI", "UAE Central Bank / CBUAE AML-CFT", "OPEC Secretariat"],
        "compliance_vector": "AIS spoofing detection, tier-1 maritime insurer vetting, and correspondent banking KYC on dirham/dollar conversion rails."
    },
    "central_asia_banking_rails": {
        "keywords": ["banking", "correspondent", "kzt", "rub", "sanctions", "secondary", "ofac", "secondary sanctions"],
        "summary": "Secondary sanctions transmission channel via Central Asian tier-1 and tier-2 commercial banks. Key scrutiny: Mir card de-linking, dual-use payment routing, third-party intermediary vetting for high-priority export control items (CHPL).",
        "primary_actors": ["National Bank of Kazakhstan", "AFMRK (Financial Monitoring Agency)", "AIFC AFSA"],
        "compliance_vector": "Real-time automated transaction screening against OFAC SDN and EU consolidated lists before SWIFT/KZT clearing."
    }
}

def lookup_regional_knowledge(topic: str) -> str:
    """Retrieve pre-compiled domain intelligence vectors matching query keywords."""
    topic_lower = topic.lower()
    matches: List[str] = []
    
    for key, entity in REGIONAL_ENTITIES_REGISTRY.items():
        if any(kw in topic_lower for kw in entity["keywords"]):
            entry = (
                f"### [PROPRIETARY DOMAIN REGISTER: {key.upper()}]\n"
                f"- Context: {entity['summary']}\n"
                f"- Primary Actors: {', '.join(entity['primary_actors'])}\n"
                f"- Mandatory Compliance Vector: {entity['compliance_vector']}"
            )
            matches.append(entry)
            
    if not matches:
        return "No specific proprietary entity matches in local registry. Defaulting to live open-stream retrieval."
        
    return "\n\n".join(matches)
