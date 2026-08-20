from typing import Protocol
from uuid import UUID

from app.models import Chunk, Collection, Document


class Repository(Protocol):
    collections: dict[UUID, Collection]
    documents: dict[UUID, Document]
    chunks: dict[UUID, Chunk]

    def collection_chunks(
        self, collection_id: UUID, workspace_id: str | None = None, user_id: str | None = None
    ) -> list[Chunk]: ...
