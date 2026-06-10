from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EvalQuestion(BaseModel):
    question: str
    ground_truth: str
    relevant_chunk_ids: list[UUID] = Field(default_factory=list)
    source_document: str | None = None


class EvalDataset(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    collection_id: UUID
    questions: list[EvalQuestion]
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EvalRun(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    dataset_id: UUID
    pipeline_config: dict[str, Any]
    status: str = "PENDING"
    faithfulness_score: float | None = None
    answer_relevancy_score: float | None = None
    context_precision_score: float | None = None
    context_recall_score: float | None = None
    hallucination_rate: float | None = None
    avg_latency_ms: int | None = None
    avg_cost_usd: float | None = None
    total_questions: int | None = None
    results: dict[str, Any] | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: datetime | None = None
