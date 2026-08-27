"""FastAPI server for Global Think Tank Analyst."""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

try:
    from .agent import AnalystAgent
except ImportError:
    AnalystAgent = None

app = FastAPI(
    title="Global Think Tank Analyst API",
    description="Enterprise REST API for Strategic-Risk Memo Generation",
    version="1.5.0"
)

# We lazy-load the agent so the app can be imported without env vars,
# but routes will fail if dependencies/keys are missing.
_agent_instance = None

def get_agent():
    global _agent_instance
    if _agent_instance is None:
        if AnalystAgent is None:
            raise HTTPException(status_code=500, detail="Agent dependencies missing. Run pip install global-think-tank-analyst[agent,enterprise]")
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable is required.")
        _agent_instance = AnalystAgent()
    return _agent_instance

class MemoRequest(BaseModel):
    topic: str
    mode: str = "B"
    thread_id: str = "default_thread"

class MemoResponse(BaseModel):
    thread_id: str
    memo: str

@app.post("/api/v1/memo", response_model=MemoResponse)
async def generate_memo(req: MemoRequest):
    """Generate a strategic-risk memo using the LangGraph Multi-Agent pipeline."""
    agent = get_agent()
    try:
        # Agent now supports thread_id for memory
        result = agent.generate_memo(topic=req.topic, mode=req.mode, thread_id=req.thread_id)
        return MemoResponse(thread_id=req.thread_id, memo=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
