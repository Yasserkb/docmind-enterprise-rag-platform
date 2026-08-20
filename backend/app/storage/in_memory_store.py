from uuid import UUID

from app.models import AgentRun, Chunk, Collection, Document, EvalDataset, EvalRun, QueryLog


class InMemoryStore:
    def __init__(self):
        self.collections: dict[UUID, Collection] = {}
        self.documents: dict[UUID, Document] = {}
        self.chunks: dict[UUID, Chunk] = {}
        self.query_logs: dict[UUID, QueryLog] = {}
        self.eval_datasets: dict[UUID, EvalDataset] = {}
        self.eval_runs: dict[UUID, EvalRun] = {}
        self.agent_runs: dict[UUID, AgentRun] = {}

    def add_collection(self, collection: Collection) -> Collection:
        collection.qdrant_collection_name = collection.qdrant_collection_name or f"docmind_{collection.id.hex}"
        collection.es_index_name = collection.es_index_name or f"docmind_{collection.id.hex}_chunks"
        self.collections[collection.id] = collection
        return collection

    def add_chunks(self, chunks: list[Chunk]) -> None:
        for chunk in chunks:
            self.chunks[chunk.id] = chunk
        if chunks:
            collection = self.collections[chunks[0].collection_id]
            collection.document_count = len([doc for doc in self.documents.values() if doc.collection_id == collection.id])

    def collection_chunks(
        self, collection_id: UUID, workspace_id: str | None = None, user_id: str | None = None
    ) -> list[Chunk]:
        return [
            chunk
            for chunk in self.chunks.values()
            if chunk.collection_id == collection_id
            and (workspace_id is None or chunk.workspace_id == workspace_id)
            and (not chunk.allowed_user_ids or user_id in chunk.allowed_user_ids)
        ]
