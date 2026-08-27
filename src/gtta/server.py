"""FastAPI server for Global Think Tank Analyst."""

import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List

try:
    from .agent import AnalystAgent
except ImportError:
    AnalystAgent = None

from .db import init_db, add_job, update_job, get_inbox

app = FastAPI(
    title="Global Think Tank Analyst API",
    description="Enterprise REST API & Fleet Control Center",
    version="1.6.0"
)

@app.on_event("startup")
def startup_event():
    init_db()

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
    """Generate a single strategic-risk memo synchronously."""
    agent = get_agent()
    try:
        result = agent.generate_memo(topic=req.topic, mode=req.mode, thread_id=req.thread_id)
        return MemoResponse(thread_id=req.thread_id, memo=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ========================================================
# STAGE 3: FLEET CONTROL CENTER (Background Agents)
# ========================================================

class FleetBatchRequest(BaseModel):
    topics: List[str]
    mode: str = "B"

def process_fleet_job(job_id: int, topic: str, mode: str):
    """Background worker function for a single agent."""
    try:
        update_job(job_id, "RUNNING")
        agent = get_agent()
        # Thread ID unique to job
        result = agent.generate_memo(topic=topic, mode=mode, thread_id=f"fleet_job_{job_id}")
        update_job(job_id, "COMPLETED", result)
    except Exception as e:
        update_job(job_id, "FAILED", str(e))

@app.post("/api/v1/fleet/batch")
async def trigger_fleet(req: FleetBatchRequest, bg_tasks: BackgroundTasks):
    """Spawn a fleet of background agents to process multiple topics asynchronously."""
    job_ids = []
    for topic in req.topics:
        jid = add_job(topic)
        job_ids.append(jid)
        bg_tasks.add_task(process_fleet_job, jid, topic, req.mode)
    return {"message": f"Spawned {len(job_ids)} background agents.", "job_ids": job_ids}

@app.get("/api/v1/fleet/inbox")
def get_fleet_inbox():
    """Retrieve the status and results of all background fleet agents."""
    return get_inbox()

@app.get("/health")
def health_check():
    return {"status": "ok"}
