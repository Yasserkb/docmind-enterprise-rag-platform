# Current state

DocMind provides a FastAPI API, React UI, Spring gateway, parser/chunker adapters, deterministic embeddings and generation, hybrid lexical/vector-style retrieval, RRF, reranking, citations, evaluation metrics, Prometheus instrumentation, and a Compose stack containing PostgreSQL, Redis, Qdrant and Elasticsearch.

The default runtime is intentionally local and deterministic. Collections, documents and chunks now carry workspace scope, and API handlers apply workspace checks before retrieval. This proves the authorization boundary without pretending that trusted demo headers are production authentication. The persistent search and metadata services are present as deployment dependencies, but the default application adapter remains in-memory.
