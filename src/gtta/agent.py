"""Active RAG Agent pipeline for Global Think Tank Analyst."""

import os
from typing import Optional
from .langchain import get_system_prompt

class AnalystAgent:
    def __init__(self, model_name: str = "gpt-4o", language: str = "en"):
        self.model_name = model_name
        self.language = language
        self.system_prompt = get_system_prompt(language=self.language)
        
        try:
            from langchain_openai import ChatOpenAI
            from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
            from langchain.agents import create_openai_tools_agent, AgentExecutor
            from langchain_community.tools import DuckDuckGoSearchResults
        except ImportError:
            raise ImportError(
                "Agent dependencies missing. Install them via: pip install global-think-tank-analyst[agent]"
            )
            
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required.")
            
        # Initialize the LLM
        self.llm = ChatOpenAI(model=self.model_name, temperature=0.2)
        
        # Tools: We use DuckDuckGo as a free search alternative
        self.tools = [DuckDuckGoSearchResults()]
        
        # Build the prompt
        prompt = ChatPromptTemplate.from_messages([
            self.system_prompt,
            ("user", "Please analyze the following topic using your skills and available tools to retrieve current information.\nTopic: {input}\nMode: {mode}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create Agent
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def generate_memo(self, topic: str, mode: str = "B") -> str:
        """
        Orchestrate the creation of a memo.
        1. Retrieve sources via DuckDuckGo.
        2. Format context.
        3. Invoke LLM with the SKILL.md system prompt.
        """
        result = self.agent_executor.invoke({"input": topic, "mode": f"Mode {mode}"})
        return result["output"]
