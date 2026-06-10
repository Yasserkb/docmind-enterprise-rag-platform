from uuid import UUID

from app.ingestion.embeddings import EmbeddingService, cosine
from app.models import Chunk


class SemanticSearchClient:
    """Local vector-search adapter with a Qdrant-compatible boundary."""

    def __init__(self):
        self.embeddings = EmbeddingService()

    def search(self, query: str, collection_id: UUID, chunks: list[Chunk], top_k: int = 20) -> list[tuple[Chunk, float]]:
        query_vector = self.embeddings.embed(query)
        scored = [(chunk, cosine(query_vector, chunk.embedding or [])) for chunk in chunks if chunk.collection_id == collection_id]
        return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]
