from app.generation.rag_pipeline import RagPipeline
from app.ingestion.pipeline import IngestionPipeline
from app.models import Collection, QueryRequest, SourceType
from app.storage.in_memory_store import InMemoryStore


def test_rag_pipeline_returns_answer_and_sources():
    store = InMemoryStore()
    collection = store.add_collection(Collection(name="Policies"))
    IngestionPipeline(store).ingest_bytes(collection, "policy.txt", SourceType.TXT, b"Daily transaction limit is EUR 50000.", {})
    response = RagPipeline(store).run(QueryRequest(question="What is the transaction limit?", collection_id=collection.id))
    assert response.answer
    assert response.sources
