"""FastAPI server for Global Think Tank Analyst."""

import logging
import os
import secrets
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

try:
    from .agent import AnalystAgent
except ImportError:
    AnalystAgent = None

from .db import init_db, add_job, update_job, get_inbox

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Global Think Tank Analyst API",
    description="REST API and fleet control centre for structured strategic-risk memos",
    version="1.6.0"
)

# Every memo endpoint spends model credits on the operator's key, so the route is
# gated whenever GTTA_API_KEY is set: callers must send `Authorization: Bearer <key>`.
# Leaving it unset keeps a local demo callable, and the server says so at startup
# rather than failing open silently.
_bearer = HTTPBearer(auto_error=False)


def require_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> None:
    expected = os.getenv("GTTA_API_KEY")
    if not expected:
        return
    supplied = credentials.credentials if credentials else ""
    # Constant-time compare so a wrong key cannot be recovered from response timing.
    if not secrets.compare_digest(supplied, expected):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.on_event("startup")
def startup_event():
    init_db()
    if not os.getenv("GTTA_API_KEY"):
        logger.warning(
            "GTTA_API_KEY is not set: the memo and fleet routes are open to anyone who "
            "can reach this port, and each call spends model credits. Set GTTA_API_KEY "
            "to require a bearer token, and bind to a private interface."
        )

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
    economics: Optional[dict] = None
    iterations: Optional[int] = 1

@app.post("/api/v1/memo", response_model=MemoResponse, dependencies=[Depends(require_api_key)])
async def generate_memo(req: MemoRequest):
    """Generate a single strategic-risk memo synchronously with Unit Economics."""
    agent = get_agent()
    try:
        data = agent.generate_memo_with_metrics(topic=req.topic, mode=req.mode, thread_id=req.thread_id)
        return MemoResponse(
            thread_id=req.thread_id,
            memo=data["memo"],
            economics=data["economics"],
            iterations=data["iterations"]
        )
    except Exception:
        logger.exception("Memo generation failed")
        raise HTTPException(status_code=500, detail="Memo generation failed")

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

@app.post("/api/v1/fleet/batch", dependencies=[Depends(require_api_key)])
async def trigger_fleet(req: FleetBatchRequest, bg_tasks: BackgroundTasks):
    """Spawn a fleet of background agents to process multiple topics asynchronously."""
    job_ids = []
    for topic in req.topics:
        jid = add_job(topic)
        job_ids.append(jid)
        bg_tasks.add_task(process_fleet_job, jid, topic, req.mode)
    return {"message": f"Spawned {len(job_ids)} background agents.", "job_ids": job_ids}

@app.get("/api/v1/fleet/inbox", dependencies=[Depends(require_api_key)])
def get_fleet_inbox():
    """Retrieve the status and results of all background fleet agents."""
    return get_inbox()

@app.get("/health")
def health_check():
    return {"status": "ok"}
