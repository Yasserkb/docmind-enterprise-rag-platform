# DocMind Architecture

DocMind is a modular RAG application split into API, ingestion, retrieval, generation, evaluation, observability, frontend, gateway and infrastructure layers.

The local implementation uses deterministic adapters so the platform can run without external AI keys. The boundaries mirror production adapters for embeddings, LLM calls, vector stores, keyword search, reranking and persistence.
