from app.ingestion.pipeline import IngestionPipeline
from app.models import Collection, SourceType
from app.retrieval.hybrid_search import HybridSearchEngine
from app.storage.in_memory_store import InMemoryStore


def test_hybrid_search_returns_relevant_chunk():
    store = InMemoryStore()
    collection = store.add_collection(Collection(name="Policies"))
    IngestionPipeline(store).ingest_bytes(collection, "policy.txt", SourceType.TXT, b"Daily transaction limit is EUR 50000.", {})
    results = HybridSearchEngine().search("transaction limit", collection.id, store.collection_chunks(collection.id))
    assert results
