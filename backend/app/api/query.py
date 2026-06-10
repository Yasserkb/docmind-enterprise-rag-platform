from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.generation.rag_pipeline import RagPipeline
from app.models import QueryLog, QueryRequest, QueryResponse
from app.storage.store import store

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest) -> QueryResponse:
    if req.collection_id not in store.collections:
        raise HTTPException(404, "Collection not found")
    return RagPipeline(store).run(req)


@router.post("/query/stream")
def query_stream(req: QueryRequest) -> StreamingResponse:
    response = RagPipeline(store).run(req)

    def stream_tokens():
        for token in response.answer.split():
            yield f"data: {token}\n\n"
        yield "event: done\ndata: [DONE]\n\n"

    return StreamingResponse(stream_tokens(), media_type="text/event-stream")


@router.get("/query/history", response_model=list[QueryLog])
def query_history() -> list[QueryLog]:
    return sorted(store.query_logs.values(), key=lambda item: item.created_at, reverse=True)


@router.get("/query/{query_id}", response_model=QueryLog)
def get_query(query_id: UUID) -> QueryLog:
    if query_id not in store.query_logs:
        raise HTTPException(404, "Query not found")
    return store.query_logs[query_id]
