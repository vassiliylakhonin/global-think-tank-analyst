"""Unit Economics, Cost Tracking, and Model Routing for Global Think Tank Analyst."""

from typing import Dict, Any

# Price per 1 Million tokens (USD) based on market index
MODEL_PRICING: Dict[str, Dict[str, float]] = {
    # Open-weight / Fast Tier (Tier 1 - Extraction & Search)
    "deepseek-chat": {"input": 0.14, "output": 0.28},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    
    # Frontier Tier (Tier 2 - Synthesis, Red-Team & Legal Discipline)
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "deepseek-reasoner": {"input": 0.55, "output": 2.19},
}

DEFAULT_B2B_PRICE_PER_MEMO_USD = 25.00  # Target enterprise SaaS value per decision pack

def estimate_tokens(text: str) -> int:
    """Fast heuristic token counter (~4 chars per token)."""
    return max(1, len(text) // 4)

def calculate_cost(input_tokens: int, output_tokens: int, model_name: str = "gpt-4o-mini") -> float:
    """Calculate exact USD cost for a model execution."""
    pricing = MODEL_PRICING.get(model_name, MODEL_PRICING["gpt-4o-mini"])
    cost = (input_tokens / 1_000_000 * pricing["input"]) + (output_tokens / 1_000_000 * pricing["output"])
    return round(cost, 6)

def calculate_unit_economics(
    input_text: str,
    output_text: str,
    fast_model: str = "gpt-4o-mini",
    frontier_model: str = "gpt-4o",
    b2b_unit_price: float = DEFAULT_B2B_PRICE_PER_MEMO_USD
) -> Dict[str, Any]:
    """
    Calculate comprehensive unit economics for an agent execution run,
    comparing Model Cascading savings vs pure Frontier pricing.
    """
    in_tokens = estimate_tokens(input_text)
    out_tokens = estimate_tokens(output_text)
    
    # Cascaded cost (Fast extraction + Frontier critique/synthesis)
    cascaded_cost = calculate_cost(in_tokens // 2, out_tokens // 2, fast_model) + \
                    calculate_cost(in_tokens // 2, out_tokens // 2, frontier_model)
    
    # Baseline pure frontier cost
    frontier_only_cost = calculate_cost(in_tokens, out_tokens, frontier_model)
    
    savings_pct = round(((frontier_only_cost - cascaded_cost) / max(frontier_only_cost, 0.000001)) * 100, 1)
    gross_margin_pct = round(((b2b_unit_price - cascaded_cost) / b2b_unit_price) * 100, 2)
    
    return {
        "estimated_input_tokens": in_tokens,
        "estimated_output_tokens": out_tokens,
        "total_tokens": in_tokens + out_tokens,
        "query_cost_usd": cascaded_cost,
        "pure_frontier_cost_usd": frontier_only_cost,
        "cascading_savings_pct": max(0.0, savings_pct),
        "gross_margin_pct": gross_margin_pct,
        "b2b_unit_value_usd": b2b_unit_price,
        "routing_strategy": f"Cascade: {fast_model} (Scrape/Graph) -> {frontier_model} (Critic/Red-Team)"
    }
