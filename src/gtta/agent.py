"""Experimental search, drafting, diagram extraction, and critique pipeline."""

import os
from typing import TypedDict, Dict, Any, Optional
from .economics import calculate_unit_economics
from .knowledge import lookup_regional_knowledge


class AgentState(TypedDict):
    topic: str
    mode: str
    research_data: str
    graph_data: str
    draft: str
    critique: str
    validation_passed: bool
    final_memo: str
    iterations: int
    economics: Dict[str, Any]


class AnalystAgent:
    def __init__(
        self,
        frontier_model: str = "gpt-4o",
        fast_model: str = "gpt-4o-mini",
        language: str = "en",
    ):
        self.frontier_model = frontier_model
        self.fast_model = fast_model
        self.language = language

        try:
            from .langchain import get_system_prompt
            from langchain_openai import ChatOpenAI
            from langgraph.graph import StateGraph, END
            from langgraph.checkpoint.memory import MemorySaver
            from langchain_community.tools import DuckDuckGoSearchResults
        except ImportError as exc:
            raise ImportError(
                "Agent dependencies missing. Run: pip install global-think-tank-analyst[agent]"
            ) from exc

        self.system_prompt = get_system_prompt(language=self.language).content

        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required.")

        # Model Cascading: Fast model for extraction, Frontier model for analytical synthesis & critique
        self.llm_fast = ChatOpenAI(model=self.fast_model, temperature=0.0)
        self.llm_frontier = ChatOpenAI(model=self.frontier_model, temperature=0.2)

        self.search_tool = DuckDuckGoSearchResults()
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

        workflow.add_conditional_edges(
            "critic", self._route_critique, {"revise": "editor", "finish": END}
        )
        workflow.add_edge("editor", "critic")

        self.graph = workflow.compile(checkpointer=self.memory)

    def _node_researcher(self, state: AgentState):
        topic = state["topic"]
        print(f"--- [Researcher / Cascade Tier 1] Gathering data for: {topic} ---")

        # 1. Query the small illustrative context registry.
        regional_context = lookup_regional_knowledge(topic)

        # 2. Live stream search
        search_results = self.search_tool.invoke(
            f"latest news policy geopolitics {topic}"
        )

        data = f"{regional_context}\n\n" f"LIVE SEARCH RESULTS:\n{search_results}"
        return {"research_data": data, "iterations": 0}

    def _node_graph_extractor(self, state: AgentState):
        print(
            f"--- [Graph Extractor / Fast Tier: {self.fast_model}] Extracting Knowledge Graph ---"
        )
        prompt = (
            f"Extract key entities (countries, companies, sanctions, policies) and their relationships "
            f"from the following research data.\n\n"
            f"Output ONLY a valid mermaid.js flowchart showing how they are connected. Do not include markdown code blocks.\n\n"
            f"Data:\n{state['research_data']}"
        )
        # Use Fast model for structured extraction (Cascade cost optimization)
        response = self.llm_fast.invoke(prompt)
        mermaid_clean = (
            response.content.replace("```mermaid", "").replace("```", "").strip()
        )
        return {"graph_data": mermaid_clean}

    def _node_drafter(self, state: AgentState):
        print(
            f"--- [Drafter / Frontier Tier: {self.frontier_model}] Drafting Strategy Memo ---"
        )
        prompt = (
            f"SYSTEM: {self.system_prompt}\n\n"
            f"You are the Drafter. Write a Mode {state['mode']} memo on '{state['topic']}'.\n"
            f"Use the following evidence:\n{state['research_data']}\n\n"
            f"Also, embed this Knowledge Graph exactly as a mermaid block in your memo:\n"
            f"```mermaid\n{state['graph_data']}\n```"
        )
        response = self.llm_frontier.invoke(prompt)
        return {"draft": response.content}

    def _node_critic(self, state: AgentState):
        print(
            f"--- [Critic / Frontier Red-Team: {self.frontier_model}] Evaluating Evidence Discipline (Iteration {state['iterations']}) ---"
        )
        prompt = (
            f"You are a strict Red-Teamer and Editor for the Global Think Tank Analyst.\n"
            f"Review the draft memo against Evidence Discipline rules.\n"
            f"Rules:\n1. Must separate Facts vs Assessments.\n2. Must have [primary]/[secondary] tags.\n3. Must avoid source theater.\n\n"
            f"Draft:\n{state['draft']}\n\n"
            f"If it passes, reply EXACTLY with 'PASS'. Otherwise, list ruthless criticisms."
        )
        response = self.llm_frontier.invoke(prompt)
        critique = response.content.strip()
        return {
            "critique": critique,
            "validation_passed": critique == "PASS",
            "iterations": state["iterations"] + 1,
        }

    def _route_critique(self, state: AgentState):
        if state.get("validation_passed", False) or state["iterations"] >= 2:
            return "finish"
        return "revise"

    def _node_editor(self, state: AgentState):
        print(
            f"--- [Editor / Frontier Tier: {self.frontier_model}] Revising based on criticism ---"
        )
        prompt = (
            f"SYSTEM: {self.system_prompt}\n\n"
            f"Fix this draft based on the Critic's feedback.\n"
            f"Draft:\n{state['draft']}\n\n"
            f"Criticism:\n{state['critique']}\n\n"
            f"Provide ONLY the revised Markdown memo."
        )
        response = self.llm_frontier.invoke(prompt)
        return {"draft": response.content}

    def generate_memo_with_metrics(
        self, topic: str, mode: str = "B", thread_id: str = "default"
    ) -> Dict[str, Any]:
        """Run the pipeline and return a memo draft with cost estimates."""
        initial_state = {
            "topic": topic,
            "mode": mode,
            "research_data": "",
            "graph_data": "",
            "draft": "",
            "critique": "",
            "validation_passed": False,
            "final_memo": "",
            "iterations": 0,
            "economics": {},
        }
        config = {"configurable": {"thread_id": thread_id}}
        final_state = self.graph.invoke(initial_state, config=config)
        draft = final_state["draft"]

        # Calculate a planning estimate from heuristic token counts.
        economics = calculate_unit_economics(
            input_text=topic + "\n" + final_state.get("research_data", ""),
            output_text=draft,
            fast_model=self.fast_model,
            frontier_model=self.frontier_model,
        )

        return {
            "memo": draft,
            "economics": economics,
            "iterations": final_state.get("iterations", 1),
            "validation_passed": final_state.get("validation_passed", False),
            "critique": final_state.get("critique", ""),
        }

    def generate_memo(
        self, topic: str, mode: str = "B", thread_id: str = "default"
    ) -> str:
        """Standard backwards-compatible generation returning markdown string."""
        result = self.generate_memo_with_metrics(
            topic=topic, mode=mode, thread_id=thread_id
        )
        return result["memo"]
