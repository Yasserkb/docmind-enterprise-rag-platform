from uuid import UUID


class SummarizeDocumentTool:
    name = "summarize_document"

    def __init__(self, store):
        self.store = store

    def run(self, collection_id: UUID) -> dict:
        chunks = self.store.collection_chunks(collection_id)[:3]
        summary = " ".join(chunk.content[:250] for chunk in chunks)
        return {"summary": summary or "No indexed content available."}
