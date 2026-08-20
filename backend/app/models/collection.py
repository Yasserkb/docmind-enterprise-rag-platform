from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Collection(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    workspace_id: str = "local-demo"
    created_by: str = "local-demo-user"
    description: str | None = None
    embedding_model: str = "local-hash-embedding"
    chunking_strategy: str = "semantic"
    qdrant_collection_name: str | None = None
    es_index_name: str | None = None
    document_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
