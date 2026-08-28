#!/usr/bin/env python3
"""
Stage 4: Dark Factory Worker for Global Think Tank Analyst.
Runs entirely autonomously: finds news, analyzes risks, validates via guardrails,
and publishes signals without any human review.
"""

import os
import time
import uuid
from pathlib import Path

try:
    from gtta.agent import AnalystAgent
    from langchain_community.tools import DuckDuckGoSearchResults
except ImportError:
    print("Dependencies missing. Run: pip install global-think-tank-analyst[agent]")
    exit(1)

OUT_DIR = Path("signals/autonomous")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def run_dark_factory():
    print("\n=======================================================")
    print("⬛️ [DARK FACTORY] Initializing Stage 4 Autonomous Loop...")
    print("=======================================================\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY required for autonomous execution.")
        return

    agent = AnalystAgent()
    search = DuckDuckGoSearchResults()

    print("[SYSTEM] Scanning global data streams for macro/geopolitical anomalies...")
    try:
        news = search.invoke("global geopolitical risk supply chain breaking news latest")
    except Exception as e:
        print(f"[ERROR] Stream offline: {e}")
        return
        
    print("[SYSTEM] Synthesizing action target from raw noise...")
    topic_prompt = f"Extract the single most critical supply chain, trade, or geopolitical risk from this news feed. Return ONLY a 1-sentence topic for analysis: {news}"
    topic = agent.llm_fast.invoke(topic_prompt).content.strip()
    
    print(f"\n🎯 [TARGET LOCKED] {topic}\n")
    print("⚙️  [PIPELINE] Dispatching LangGraph MoA Fleet with Model Cascading...")
    
    # The MoA graph guarantees Evidence Discipline via the internal Critic node (Guardrails)
    try:
        data = agent.generate_memo_with_metrics(topic=topic, mode="A", thread_id=f"dark_factory_{uuid.uuid4().hex[:8]}")
        memo = data["memo"]
        econ = data.get("economics", {})
    except Exception as e:
        print(f"[ERROR] Pipeline failure: {e}")
        return
    
    filename = OUT_DIR / f"signal_{int(time.time())}.md"
    content = f"# ⬛️ AUTONOMOUS SIGNAL (DARK FACTORY)\n**Target:** {topic}\n**Timestamp:** {time.ctime()}\n**Status:** Guardrails Passed. Zero Human Review.\n**Unit Cost:** ${econ.get('query_cost_usd', 0):.4f} (Margin: {econ.get('gross_margin_pct', 99)}%)\n\n---\n\n{memo}"
    filename.write_text(content)
    
    print(f"\n✅ [PUBLISHED] Analysis complete. Signal routed to: {filename}")
    print(f"📊 [UNIT ECONOMICS] Query Cost: ${econ.get('query_cost_usd', 0):.4f} | Margin: {econ.get('gross_margin_pct', 99)}% | Cascade Savings: {econ.get('cascading_savings_pct', 0)}%")
    print("⬛️ [DARK FACTORY] Cycle complete. Awaiting next trigger...")

if __name__ == "__main__":
    run_dark_factory()
