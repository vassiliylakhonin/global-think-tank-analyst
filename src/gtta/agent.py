"""Advanced RAG Agent pipeline with Memory and GraphRAG for Global Think Tank Analyst."""

import os
from typing import TypedDict
from .langchain import get_system_prompt

class AgentState(TypedDict):
    topic: str
    mode: str
    research_data: str
    graph_data: str
    draft: str
    critique: str
    final_memo: str
    iterations: int

class AnalystAgent:
    def __init__(self, model_name: str = "gpt-4o", language: str = "en"):
        self.model_name = model_name
        self.language = language
        self.system_prompt = get_system_prompt(language=self.language).content
        
        try:
            from langchain_openai import ChatOpenAI
            from langgraph.graph import StateGraph, END
            from langgraph.checkpoint.memory import MemorySaver
            from langchain_community.tools import DuckDuckGoSearchResults
            from langchain_experimental.tools import PythonREPLTool
        except ImportError:
            raise ImportError("Agent dependencies missing. Run: pip install global-think-tank-analyst[agent]")
            
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required.")
            
        self.llm = ChatOpenAI(model=self.model_name, temperature=0.2)
        self.search_tool = DuckDuckGoSearchResults()
        self.repl_tool = PythonREPLTool()
        self.memory = MemorySaver()
        
        # Build LangGraph
        workflow = StateGraph(AgentState)
        
        workflow.add_node("researcher", self._node_researcher)
        workflow.add_node("graph_extractor", self._node_graph_extractor)
        workflow.add_node("drafter", self._node_drafter)
        workflow.add_node("critic", self._node_critic)
        workflow.add_node("editor", self._node_editor)
        
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher", "graph_extractor")
        workflow.add_edge("graph_extractor", "drafter")
        workflow.add_edge("drafter", "critic")
        
        # Conditional edge: if critique is clean or max iterations reached, end.
        workflow.add_conditional_edges(
            "critic",
            self._route_critique,
            {"revise": "editor", "finish": END}
        )
        workflow.add_edge("editor", "critic")
        
        self.graph = workflow.compile(checkpointer=self.memory)

    def _node_researcher(self, state: AgentState):
        topic = state["topic"]
        print(f"--- [Researcher] Gathering data for: {topic} ---")
        search_results = self.search_tool.invoke(f"latest news policy geopolitics {topic}")
        code = f"print('Simulated quantitative macro data fetching for: {topic}')"
        quant_results = self.repl_tool.invoke(code)
        
        data = f"SEARCH RESULTS:\n{search_results}\n\nQUANT/CODE RESULTS:\n{quant_results}"
        return {"research_data": data, "iterations": 0}

    def _node_graph_extractor(self, state: AgentState):
        print("--- [Graph Extractor] Building Knowledge Graph (Mermaid) ---")
        prompt = (
            f"Extract key entities (countries, companies, sanctions, policies) and their relationships "
            f"from the following research data.\n\n"
            f"Output ONLY a valid mermaid.js flowchart showing how they are connected. Do not include markdown code blocks.\n\n"
            f"Data:\n{state['research_data']}"
        )
        response = self.llm.invoke(prompt)
        mermaid_clean = response.content.replace('```mermaid', '').replace('```', '').strip()
        return {"graph_data": mermaid_clean}

    def _node_drafter(self, state: AgentState):
        print("--- [Drafter] Writing initial memo ---")
        prompt = (
            f"SYSTEM: {self.system_prompt}\n\n"
            f"You are the Drafter. Write a Mode {state['mode']} memo on '{state['topic']}'.\n"
            f"Use the following evidence:\n{state['research_data']}\n\n"
            f"Also, embed this Knowledge Graph exactly as a mermaid block in your memo:\n"
            f"```mermaid\n{state['graph_data']}\n```"
        )
        response = self.llm.invoke(prompt)
        return {"draft": response.content}

    def _node_critic(self, state: AgentState):
        print(f"--- [Critic] Red-teaming draft (Iteration {state['iterations']}) ---")
        prompt = (
            f"You are a strict Red-Teamer and Editor for the Global Think Tank Analyst.\n"
            f"Review the draft memo against Evidence Discipline rules.\n"
            f"Rules:\n1. Must separate Facts vs Assessments.\n2. Must have [primary]/[secondary] tags.\n\n"
            f"Draft:\n{state['draft']}\n\n"
            f"If it passes, reply EXACTLY with 'PASS'. Otherwise, list ruthless criticisms."
        )
        response = self.llm.invoke(prompt)
        return {"critique": response.content.strip(), "iterations": state["iterations"] + 1}

    def _route_critique(self, state: AgentState):
        if state["critique"] == "PASS" or state["iterations"] >= 2:
            return "finish"
        return "revise"

    def _node_editor(self, state: AgentState):
        print("--- [Editor] Revising based on criticism ---")
        prompt = (
            f"SYSTEM: {self.system_prompt}\n\n"
            f"Fix this draft based on the Critic's feedback.\n"
            f"Draft:\n{state['draft']}\n\n"
            f"Criticism:\n{state['critique']}\n\n"
            f"Provide ONLY the revised Markdown memo."
        )
        response = self.llm.invoke(prompt)
        return {"draft": response.content}

    def generate_memo(self, topic: str, mode: str = "B", thread_id: str = "default") -> str:
        """Run the LangGraph pipeline with Memory."""
        initial_state = {
            "topic": topic, 
            "mode": mode, 
            "research_data": "", 
            "graph_data": "",
            "draft": "", 
            "critique": "", 
            "final_memo": "", 
            "iterations": 0
        }
        # Execute with thread_id for conversational memory
        config = {"configurable": {"thread_id": thread_id}}
        final_state = self.graph.invoke(initial_state, config=config)
        return final_state["draft"]
