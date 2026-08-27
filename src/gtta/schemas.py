from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Risk(BaseModel):
    name: str = Field(..., description="The name of the risk")
    severity: Literal["Low", "Moderate", "High"] = Field(..., description="Risk severity globally")
    relevance: Literal["Low", "Moderate", "High"] = Field(..., description="Risk relevance to the decision maker")
    description: str = Field(..., description="Description of the risk and trade-offs")

class Option(BaseModel):
    name: str = Field(..., description="Option name")
    description: str = Field(..., description="What it does")
    benefit: str = Field(..., description="Intended benefit")
    downside: str = Field(..., description="Main downside or cost")
    conditions: str = Field(..., description="Conditions under which it is sensible")

class Indicator(BaseModel):
    name: str = Field(..., description="Observable indicator to watch")
    trigger: str = Field(..., description="What trigger should change posture")

class StandardMemo(BaseModel):
    executive_takeaway: str = Field(..., description="Clearest plain-language answer")
    decision_context: str = Field(..., description="Decision being supported, audience, time horizon")
    knowns_and_limits: str = Field(..., description="Facts, assumptions, and unknowns")
    actors_and_incentives: str = Field(..., description="Relevant actors and their incentives")
    main_assessment: str = Field(..., description="Core analytical judgment")
    risks_and_tradeoffs: List[Risk] = Field(..., description="Material risks")
    options: List[Option] = Field(..., description="Conditional, feasible options")
    indicators: List[Indicator] = Field(..., description="Observable, decision-relevant indicators")
    confidence_level: Literal["Low", "Moderate", "High"] = Field(..., description="Confidence level")
    key_unknowns: str = Field(..., description="Key unknowns and what would change the judgment")
