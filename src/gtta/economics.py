"""Transparent model-cost estimates for Global Think Tank Analyst.

These helpers do not receive provider billing telemetry. Token counts and prices
are estimates and must not be presented as invoices, revenue, or gross margin.
"""

from typing import Dict, Any

# Illustrative price snapshot per one million tokens (USD). Operators should
# replace or update this table before using the estimate for planning.
PRICING_SNAPSHOT_DATE = "2024-08-01"
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


def estimate_tokens(text: str) -> int:
    """Fast heuristic token counter (~4 chars per token)."""
    return max(1, len(text) // 4)


def calculate_cost(
    input_tokens: int, output_tokens: int, model_name: str = "gpt-4o-mini"
) -> float:
    """Estimate USD cost from heuristic token counts and a price snapshot."""
    pricing = MODEL_PRICING.get(model_name, MODEL_PRICING["gpt-4o-mini"])
    cost = (input_tokens / 1_000_000 * pricing["input"]) + (
        output_tokens / 1_000_000 * pricing["output"]
    )
    return round(cost, 6)


def calculate_unit_economics(
    input_text: str,
    output_text: str,
    fast_model: str = "gpt-4o-mini",
    frontier_model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    Estimate model cost for an execution and compare it with a simplified
    all-frontier baseline. This is planning telemetry, not billing telemetry.
    """
    in_tokens = estimate_tokens(input_text)
    out_tokens = estimate_tokens(output_text)

    # Cascaded cost (Fast extraction + Frontier critique/synthesis)
    cascaded_cost = calculate_cost(
        in_tokens // 2, out_tokens // 2, fast_model
    ) + calculate_cost(in_tokens // 2, out_tokens // 2, frontier_model)

    # Baseline pure frontier cost
    frontier_only_cost = calculate_cost(in_tokens, out_tokens, frontier_model)

    savings_pct = round(
        ((frontier_only_cost - cascaded_cost) / max(frontier_only_cost, 0.000001))
        * 100,
        1,
    )

    return {
        "estimated_input_tokens": in_tokens,
        "estimated_output_tokens": out_tokens,
        "total_tokens": in_tokens + out_tokens,
        "estimated_query_cost_usd": cascaded_cost,
        "estimated_frontier_only_cost_usd": frontier_only_cost,
        "estimated_cascading_savings_pct": max(0.0, savings_pct),
        "estimation_method": "character_count_divided_by_four",
        "pricing_snapshot_date": PRICING_SNAPSHOT_DATE,
        "routing_strategy": f"Cascade: {fast_model} (Graph) -> {frontier_model} (Draft/Critic)",
    }
