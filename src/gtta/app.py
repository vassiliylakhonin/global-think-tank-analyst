import streamlit as st
import os
import requests
from gtta.langchain import get_system_prompt

st.set_page_config(page_title="Global Think Tank Analyst", layout="wide")
st.title("🌍 Global Think Tank Analyst")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    frontier_choice = st.selectbox(
        "Frontier Model (Critic/Drafter)", ["gpt-4o", "gpt-4o-mini"]
    )
    fast_choice = st.selectbox(
        "Fast Model (Graph extraction)", ["gpt-4o-mini", "gpt-4o"]
    )
    language = st.selectbox("Prompt Language", ["en", "ru"])
    st.markdown("---")
    st.markdown("**API Status:**")
    api_url = st.text_input(
        "Local API URL (if running server)", "http://localhost:8000"
    )
    server_key = st.text_input("GTTA server bearer key", type="password")

# Tabs
tab1, tab2 = st.tabs(["💬 Single Draft", "📥 Local Batch Inbox"])

# ----------------- TAB 1: SINGLE AGENT -----------------
with tab1:
    st.markdown("### Generate a Strategic-Risk Memo (Synchronous)")
    topic = st.text_area(
        "Question / Topic",
        "What does EU CBAM enforcement-phase exposure change for a Kazakh metals exporter over the next 12 months?",
    )
    mode = st.selectbox(
        "Memo Mode",
        [
            "A - Quick Brief",
            "B - Standard Memo",
            "C - Scenario Note",
            "D - Red-Team / Contrarian",
            "E - Decision Briefing Pack",
        ],
    )
    mode_letter = mode.split(" ")[0]

    if st.button("Generate Memo"):
        if not api_key:
            st.error("Please enter an API Key in the sidebar.")
        else:
            with st.spinner(
                "Agent is gathering search results, drafting, and running an automated critique..."
            ):
                try:
                    from gtta.agent import AnalystAgent

                    agent = AnalystAgent(
                        frontier_model=frontier_choice,
                        fast_model=fast_choice,
                        language=language,
                    )
                    result_data = agent.generate_memo_with_metrics(
                        topic=topic, mode=mode_letter, thread_id="ui_thread_1"
                    )

                    # Display transparent planning estimates.
                    econ = result_data.get("economics", {})
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric(
                        "Estimated Query Cost",
                        f"${econ.get('estimated_query_cost_usd', 0.0):.4f}",
                    )
                    col2.metric(
                        "Validation",
                        "PASS" if result_data.get("validation_passed") else "REVIEW",
                    )
                    col3.metric("Tokens", f"{econ.get('total_tokens', 0):,}")
                    col4.metric(
                        "Estimated Savings",
                        f"{econ.get('estimated_cascading_savings_pct', 0)}%",
                    )

                    st.info(
                        f"**Strategy:** {econ.get('routing_strategy', '')} | Iterations: {result_data.get('iterations', 1)}"
                    )
                    st.markdown("---")
                    st.markdown(result_data["memo"])
                    if not result_data.get("validation_passed"):
                        st.warning(
                            "The critic did not return PASS. Treat this as a draft requiring human review."
                        )
                except Exception as e:
                    st.error(f"Error: {e}")

# ----------------- TAB 2: LOCAL BATCH INBOX -----------------
with tab2:
    st.markdown("### In-process Batch Inbox (Experimental)")
    st.markdown(
        "Submit up to 20 topics. Jobs run in the API process and can be interrupted by a restart; this is not a durable distributed queue."
    )

    batch_topics = st.text_area(
        "Enter topics (one per line):",
        "Impact of Red Sea attacks on European logistics\nImpact of US Semiconductor bans on Chinese startups",
    )

    if st.button("Queue Batch"):
        topics_list = [t.strip() for t in batch_topics.split("\n") if t.strip()]
        if not topics_list:
            st.warning("Enter at least one topic.")
        else:
            try:
                # Send to FastAPI background endpoint
                res = requests.post(
                    f"{api_url}/api/v1/fleet/batch",
                    json={"topics": topics_list, "mode": "B"},
                    headers={"Authorization": f"Bearer {server_key}"},
                    timeout=30,
                )
                if res.status_code == 200:
                    st.success(res.json()["message"])
                else:
                    st.error(f"API Error: {res.text}")
            except Exception as e:
                st.error(
                    f"Could not connect to API server at {api_url}. Make sure you run `gtta server` in another terminal. Error: {e}"
                )

    st.markdown("---")
    st.subheader("Agent Inbox")

    if st.button("Refresh Inbox"):
        st.rerun()

    try:
        inbox_response = requests.get(
            f"{api_url}/api/v1/fleet/inbox",
            headers={"Authorization": f"Bearer {server_key}"},
            timeout=15,
        )
        inbox_response.raise_for_status()
        inbox = inbox_response.json()
        if not inbox:
            st.info("No jobs in inbox.")
        for job in inbox:
            with st.expander(
                f"[{job['status']}] ID: {job['id']} | {job['topic'][:50]}..."
            ):
                st.text(f"Created: {job['created_at']}")
                if job["status"] == "COMPLETED":
                    st.markdown(job["result"])
                elif job["status"] == "FAILED":
                    st.error(job["result"])
                else:
                    st.info("Agent is still working...")
    except Exception as e:
        st.error(f"Could not load local Inbox DB: {e}")
