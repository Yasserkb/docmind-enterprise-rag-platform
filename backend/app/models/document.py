from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from app.models.common import DocumentStatus, SourceType


class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    collection_id: UUID
    source_type: SourceType
    source_uri: str | None = None
    content_hash: str
    status: DocumentStatus = DocumentStatus.PENDING
    language: str = "en"
    page_count: int = 1
    metadata: dict[str, Any] = Field(default_factory=dict)
    error_message: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    indexed_at: datetime | None = None
