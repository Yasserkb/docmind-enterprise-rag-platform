from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.agent.document_agent import DocumentAnalysisAgent
from app.api.schemas import AgentRunRequest
from app.models import AgentRun
from app.storage.store import store

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/run", response_model=AgentRun)
def run_agent(req: AgentRunRequest) -> AgentRun:
    if req.collection_id not in store.collections:
        raise HTTPException(404, "Collection not found")
    return DocumentAnalysisAgent(store).run(req.task, req.collection_id)


@router.get("/runs/{run_id}", response_model=AgentRun)
def get_agent_run(run_id: UUID) -> AgentRun:
    if run_id not in store.agent_runs:
        raise HTTPException(404, "Agent run not found")
    return store.agent_runs[run_id]
