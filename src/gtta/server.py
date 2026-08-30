"""FastAPI server for Global Think Tank Analyst."""

import logging
import os
import secrets
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, BackgroundTasks
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from . import __version__

try:
    from .agent import AnalystAgent
except ImportError:
    AnalystAgent = None

from .db import init_db, add_job, update_job, get_inbox

logger = logging.getLogger(__name__)

# Every memo endpoint spends model credits and can expose generated material.
# Protected routes therefore fail closed unless GTTA_API_KEY is configured.
_bearer = HTTPBearer(auto_error=False)


def require_api_key(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> None:
    expected = os.getenv("GTTA_API_KEY")
    if not expected:
        raise HTTPException(
            status_code=503,
            detail="GTTA_API_KEY is not configured; protected routes are disabled",
        )
    supplied = credentials.credentials if credentials else ""
    # Constant-time compare so a wrong key cannot be recovered from response timing.
    if not secrets.compare_digest(supplied, expected):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "Bearer"},
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    if not os.getenv("GTTA_API_KEY"):
        logger.error(
            "GTTA_API_KEY is not set: memo and fleet routes are disabled. "
            "Set a strong bearer key before using them."
        )
    yield


app = FastAPI(
    title="Global Think Tank Analyst API",
    description="REST API and batch-job experiment for structured strategic-risk memo drafts",
    version=__version__,
    lifespan=lifespan,
)


_agent_instance = None


def get_agent():
    global _agent_instance
    if _agent_instance is None:
        if AnalystAgent is None:
            raise HTTPException(
                status_code=500,
                detail="Agent dependencies missing. Run pip install global-think-tank-analyst[agent,enterprise]",
            )
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(
                status_code=500,
                detail="OPENAI_API_KEY environment variable is required.",
            )
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
    validation_passed: bool = False
    critique: Optional[str] = None
    human_review_required: bool = True


@app.post(
    "/api/v1/memo", response_model=MemoResponse, dependencies=[Depends(require_api_key)]
)
async def generate_memo(req: MemoRequest):
    """Generate a single strategic-risk memo draft with cost estimates."""
    agent = get_agent()
    try:
        data = agent.generate_memo_with_metrics(
            topic=req.topic, mode=req.mode, thread_id=req.thread_id
        )
        return MemoResponse(
            thread_id=req.thread_id,
            memo=data["memo"],
            economics=data["economics"],
            iterations=data["iterations"],
            validation_passed=data["validation_passed"],
            critique=data.get("critique"),
            human_review_required=True,
        )
    except Exception:
        logger.exception("Memo generation failed")
        raise HTTPException(status_code=500, detail="Memo generation failed")


# ========================================================
# LEGACY FLEET ROUTES: BOUNDED IN-PROCESS BATCH JOBS
# ========================================================


class FleetBatchRequest(BaseModel):
    topics: List[str]
    mode: str = "B"


def process_fleet_job(job_id: int, topic: str, mode: str):
    """Run one best-effort job in the API process."""
    try:
        update_job(job_id, "RUNNING")
        agent = get_agent()
        # Thread ID unique to job
        result = agent.generate_memo(
            topic=topic, mode=mode, thread_id=f"fleet_job_{job_id}"
        )
        update_job(job_id, "COMPLETED", result)
    except Exception as e:
        update_job(job_id, "FAILED", str(e))


@app.post("/api/v1/fleet/batch", dependencies=[Depends(require_api_key)])
async def trigger_fleet(req: FleetBatchRequest, bg_tasks: BackgroundTasks):
    """Queue a bounded batch in this API process after the response is sent."""
    if not 1 <= len(req.topics) <= 20:
        raise HTTPException(
            status_code=422, detail="topics must contain between 1 and 20 items"
        )
    if any(not topic.strip() or len(topic) > 500 for topic in req.topics):
        raise HTTPException(
            status_code=422, detail="each topic must be 1-500 characters"
        )
    job_ids = []
    for topic in req.topics:
        jid = add_job(topic)
        job_ids.append(jid)
        bg_tasks.add_task(process_fleet_job, jid, topic, req.mode)
    return {
        "message": f"Queued {len(job_ids)} in-process background jobs.",
        "job_ids": job_ids,
        "durable": False,
    }


@app.get("/api/v1/fleet/inbox", dependencies=[Depends(require_api_key)])
def get_fleet_inbox():
    """Retrieve statuses and results from the local batch inbox."""
    return get_inbox()


@app.get("/health")
def health_check():
    return {"status": "ok"}
