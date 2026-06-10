from uuid import UUID

from pydantic import BaseModel, Field

from app.models import EvalQuestion


class CreateCollectionRequest(BaseModel):
    name: str
    description: str | None = None
    embedding_model: str = "local-hash-embedding"
    chunking_strategy: str = "semantic"


class IngestUrlRequest(BaseModel):
    url: str
    metadata: dict = Field(default_factory=dict)


class IngestS3Request(BaseModel):
    bucket: str
    key: str
    metadata: dict = Field(default_factory=dict)


class CreateDatasetRequest(BaseModel):
    name: str
    collection_id: UUID
    questions: list[EvalQuestion]


class CreateEvalRunRequest(BaseModel):
    name: str
    dataset_id: UUID
    pipeline_config: dict


class AgentRunRequest(BaseModel):
    collection_id: UUID
    task: str
