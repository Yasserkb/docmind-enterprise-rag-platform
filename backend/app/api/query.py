from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.generation.rag_pipeline import RagPipeline
from app.core.security import RequestIdentity, current_identity
from app.models import QueryLog, QueryRequest, QueryResponse
from app.storage.store import store

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest, identity: RequestIdentity = Depends(current_identity)) -> QueryResponse:
    collection = store.collections.get(req.collection_id)
    if not collection or collection.workspace_id != identity.workspace_id:
        raise HTTPException(404, "Collection not found")
    return RagPipeline(store).run(req, identity.workspace_id, identity.user_id)


@router.post("/query/stream")
def query_stream(req: QueryRequest, identity: RequestIdentity = Depends(current_identity)) -> StreamingResponse:
    collection = store.collections.get(req.collection_id)
    if not collection or collection.workspace_id != identity.workspace_id:
        raise HTTPException(404, "Collection not found")
    response = RagPipeline(store).run(req, identity.workspace_id, identity.user_id)

    def stream_tokens():
        for token in response.answer.split():
            yield f"data: {token}\n\n"
        yield "event: done\ndata: [DONE]\n\n"

    return StreamingResponse(stream_tokens(), media_type="text/event-stream")


@router.get("/query/history", response_model=list[QueryLog])
def query_history(identity: RequestIdentity = Depends(current_identity)) -> list[QueryLog]:
    visible = [
        log for log in store.query_logs.values()
        if store.collections.get(log.collection_id)
        and store.collections[log.collection_id].workspace_id == identity.workspace_id
    ]
    return sorted(visible, key=lambda item: item.created_at, reverse=True)


@router.get("/query/{query_id}", response_model=QueryLog)
def get_query(query_id: UUID, identity: RequestIdentity = Depends(current_identity)) -> QueryLog:
    log = store.query_logs.get(query_id)
    if not log or store.collections.get(log.collection_id, None) is None or store.collections[log.collection_id].workspace_id != identity.workspace_id:
        raise HTTPException(404, "Query not found")
    return log
