from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Chunk(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    collection_id: UUID
    content: str
    chunk_index: int
    token_count: int
    start_page: int = 1
    end_page: int = 1
    heading_path: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    embedding: list[float] | None = None
