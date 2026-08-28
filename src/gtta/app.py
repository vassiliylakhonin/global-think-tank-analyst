import streamlit as st
import os
import requests
from gtta.langchain import get_system_prompt
from gtta.db import init_db, get_inbox

# Ensure DB is initialized for direct UI access
init_db()

st.set_page_config(page_title="Global Think Tank Analyst", layout="wide")
st.title("🌍 Global Think Tank Analyst")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI / Anthropic API Key", type="password")
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    frontier_choice = st.selectbox("Frontier Model (Critic/Drafter)", ["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet-20240620"])
    fast_choice = st.selectbox("Fast Model (Scraper/Graph)", ["gpt-4o-mini", "deepseek-chat", "gemini-1.5-flash"])
    language = st.selectbox("Prompt Language", ["en", "ru"])
    st.markdown("---")
    st.markdown("**API Status:**")
    api_url = st.text_input("Local API URL (if running server)", "http://localhost:8000")

# Tabs
tab1, tab2 = st.tabs(["💬 Single Agent Chat", "🚢 Fleet Control Center (Stage 3)"])

# ----------------- TAB 1: SINGLE AGENT -----------------
with tab1:
    st.markdown("### Generate a Strategic-Risk Memo (Synchronous)")
    topic = st.text_area("Question / Topic", "What does EU CBAM enforcement-phase exposure change for a Kazakh metals exporter over the next 12 months?")
    mode = st.selectbox("Memo Mode", ["A - Quick Brief", "B - Standard Memo", "C - Scenario Note", "D - Red-Team / Contrarian", "E - Decision Briefing Pack"])
    mode_letter = mode.split(" ")[0]

    if st.button("Generate Memo"):
        if not api_key:
            st.error("Please enter an API Key in the sidebar.")
        else:
            with st.spinner("Agent is cascading models, checking proprietary registry, drafting, and red-teaming..."):
                try:
                    from gtta.agent import AnalystAgent
                    agent = AnalystAgent(frontier_model=frontier_choice, fast_model=fast_choice, language=language)
                    result_data = agent.generate_memo_with_metrics(topic=topic, mode=mode_letter, thread_id="ui_thread_1")
                    
                    # Display Unit Economics Card (MA7 Slide 7 & 16)
                    econ = result_data.get("economics", {})
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Query Cost", f"${econ.get('query_cost_usd', 0.0):.4f}")
                    col2.metric("Gross Margin", f"{econ.get('gross_margin_pct', 99.0)}%")
                    col3.metric("Tokens", f"{econ.get('total_tokens', 0):,}")
                    col4.metric("Cascade Savings", f"{econ.get('cascading_savings_pct', 0)}%")
                    
                    st.info(f"**Strategy:** {econ.get('routing_strategy', '')} | Iterations: {result_data.get('iterations', 1)}")
                    st.markdown("---")
                    st.markdown(result_data["memo"])
                except Exception as e:
                    st.error(f"Error: {e}")

# ----------------- TAB 2: FLEET CONTROL CENTER -----------------
with tab2:
    st.markdown("### Background Agents Inbox (Asynchronous)")
    st.markdown("Upload multiple specs/topics. The server will spawn a background agent for each, avoiding timeouts. You can leave and check the Inbox later.")
    
    batch_topics = st.text_area("Enter topics (one per line):", "Impact of Red Sea attacks on European logistics\nImpact of US Semiconductor bans on Chinese startups")
    
    if st.button("Spawn Fleet"):
        topics_list = [t.strip() for t in batch_topics.split("\n") if t.strip()]
        if not topics_list:
            st.warning("Enter at least one topic.")
        else:
            try:
                # Send to FastAPI background endpoint
                res = requests.post(
                    f"{api_url}/api/v1/fleet/batch",
                    json={"topics": topics_list, "mode": "B"}
                )
                if res.status_code == 200:
                    st.success(res.json()["message"])
                else:
                    st.error(f"API Error: {res.text}")
            except Exception as e:
                st.error(f"Could not connect to API server at {api_url}. Make sure you run `gtta server` in another terminal. Error: {e}")
    
    st.markdown("---")
    st.subheader("Agent Inbox")
    
    if st.button("Refresh Inbox"):
        st.rerun()
        
    try:
        inbox = get_inbox()
        if not inbox:
            st.info("No jobs in inbox.")
        for job in inbox:
            with st.expander(f"[{job['status']}] ID: {job['id']} | {job['topic'][:50]}..."):
                st.text(f"Created: {job['created_at']}")
                if job['status'] == "COMPLETED":
                    st.markdown(job['result'])
                elif job['status'] == "FAILED":
                    st.error(job['result'])
                else:
                    st.info("Agent is still working...")
    except Exception as e:
        st.error(f"Could not load local Inbox DB: {e}")
