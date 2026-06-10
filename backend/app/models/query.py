from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class QueryConfig(BaseModel):
    top_k: int = 5
    reranking: bool = True
    hyde: bool = True
    model: str = "local-grounded"
    stream: bool = False


class QueryRequest(BaseModel):
    question: str
    collection_id: UUID
    config: QueryConfig = Field(default_factory=QueryConfig)


class SourceCitation(BaseModel):
    document_title: str
    page: int
    chunk_id: UUID
    chunk_content: str
    relevance_score: float


class QueryMetadata(BaseModel):
    latency_ms: int
    model: str
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    retrieval_strategy: str
    chunks_retrieved: int


class QueryResponse(BaseModel):
    query_id: UUID = Field(default_factory=uuid4)
    answer: str
    sources: list[SourceCitation]
    confidence_score: float
    metadata: QueryMetadata


class QueryLog(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    collection_id: UUID
    question: str
    answer: str
    retrieved_chunk_ids: list[UUID]
    rerank_scores: dict[str, float]
    llm_model: str
    confidence_score: float
    latency_ms: int
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float
    extra: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
