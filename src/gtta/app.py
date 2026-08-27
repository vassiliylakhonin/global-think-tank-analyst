import streamlit as st
import os
from gtta.langchain import get_system_prompt

st.set_page_config(page_title="Global Think Tank Analyst", layout="wide")

st.title("🌍 Global Think Tank Analyst")
st.markdown("### Strategic-Risk Policy Memo Generator")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("OpenAI / Anthropic API Key", type="password")
    model_choice = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet-20240620"])
    language = st.selectbox("Prompt Language", ["en", "ru"])
    st.markdown("---")
    st.markdown("**Note:** This UI requires your own API key to generate memos.")

st.markdown("Enter a policy, regulatory, or geopolitical question below to generate a structured strategic-risk memo.")

topic = st.text_area("Question / Topic", "What does EU CBAM enforcement-phase exposure change for a Kazakh metals exporter over the next 12 months?")
audience = st.text_input("Audience (e.g. founder, board, policymaker)", "founder / operator")
horizon = st.text_input("Time Horizon", "12 months")
mode = st.selectbox("Memo Mode", [
    "A - Quick Brief", 
    "B - Standard Memo", 
    "C - Scenario Note", 
    "D - Red-Team / Contrarian", 
    "E - Decision Briefing Pack"
])

if st.button("Generate Memo"):
    if not api_key:
        st.error("Please enter an API Key in the sidebar.")
    else:
        st.info("Generation would start here! (Agentic retrieval & LLM calls will be wired up via the `gtta.agent` module).")
        # Here we would initialize the LangChain/LangGraph agent and stream the output.
        # For this skeleton, we just show success.
        
        system_prompt = get_system_prompt(language=language)
        
        st.success("Agent initialized with the following system instructions:")
        with st.expander("View System Prompt"):
            st.text(system_prompt.content[:1000] + "\n...[truncated]")
