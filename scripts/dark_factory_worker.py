#!/usr/bin/env python3
"""
Legacy experimental worker for Global Think Tank Analyst.
It discovers a topic and generates a draft, but never publishes without review.
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

OUT_DIR = Path("signals/review-queue")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def run_review_queue_worker():
    print("\n=======================================================")
    print("[EXPERIMENTAL WORKER] Initializing one draft cycle...")
    print("=======================================================\n")

    if not os.getenv("OPENAI_API_KEY"):
        print("[ERROR] OPENAI_API_KEY is required to generate a review draft.")
        return

    agent = AnalystAgent()
    search = DuckDuckGoSearchResults()

    print("[SYSTEM] Running one public-web topic search...")
    try:
        news = search.invoke(
            "global geopolitical risk supply chain breaking news latest"
        )
    except Exception as e:
        print(f"[ERROR] Stream offline: {e}")
        return

    print("[SYSTEM] Proposing one topic from the search output...")
    topic_prompt = f"Extract the single most critical supply chain, trade, or geopolitical risk from this news feed. Return ONLY a 1-sentence topic for analysis: {news}"
    topic = agent.llm_fast.invoke(topic_prompt).content.strip()

    print(f"\n[PROPOSED TOPIC] {topic}\n")
    print("[PIPELINE] Generating one draft and automated critique...")

    try:
        data = agent.generate_memo_with_metrics(
            topic=topic, mode="A", thread_id=f"review_queue_{uuid.uuid4().hex[:8]}"
        )
        memo = data["memo"]
        econ = data.get("economics", {})
    except Exception as e:
        print(f"[ERROR] Pipeline failure: {e}")
        return

    filename = OUT_DIR / f"signal_{int(time.time())}.md"
    validation = (
        "critic-pass" if data.get("validation_passed") else "critic-review-required"
    )
    content = (
        "# EXPERIMENTAL SIGNAL DRAFT\n"
        f"**Target:** {topic}\n"
        f"**Timestamp:** {time.ctime()}\n"
        f"**Automated critic:** {validation}\n"
        "**Publication status:** Human review required. Not published.\n"
        f"**Estimated model cost:** ${econ.get('estimated_query_cost_usd', 0):.4f}\n\n"
        f"**Critique:** {data.get('critique', '')}\n\n---\n\n{memo}"
    )
    filename.write_text(content, encoding="utf-8")

    print(f"\n[DRAFTED] Review-required analysis saved to: {filename}")
    print(f"[COST ESTIMATE] ${econ.get('estimated_query_cost_usd', 0):.4f}")
    print("[EXPERIMENTAL WORKER] Cycle complete; no publication was attempted.")


if __name__ == "__main__":
    run_review_queue_worker()
