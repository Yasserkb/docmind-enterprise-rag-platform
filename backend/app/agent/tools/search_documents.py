from uuid import UUID

from app.retrieval.hybrid_search import HybridSearchEngine


class SearchDocumentsTool:
    name = "search_documents"

    def __init__(self, store):
        self.store = store
        self.search = HybridSearchEngine()

    def run(self, query: str, collection_id: UUID, top_k: int = 5) -> list[dict]:
        chunks = self.store.collection_chunks(collection_id)
        return [
            {
                "chunk_id": str(chunk.id),
                "document_title": chunk.metadata.get("document_title", "Uploaded document"),
                "score": round(float(score), 4),
                "preview": chunk.content[:350],
            }
            for chunk, score in self.search.search(query, collection_id, chunks, top_k=top_k)
        ]
