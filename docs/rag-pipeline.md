# RAG Pipeline

1. Receive the user question.
2. Expand the query and optionally create a HyDE-style synthetic document representation.
3. Run semantic retrieval through the vector-search adapter.
4. Run keyword retrieval through the BM25-style adapter.
5. Merge results using Reciprocal Rank Fusion.
6. Rerank the top candidates.
7. Assemble context blocks with source metadata.
8. Generate a grounded answer with citations.
9. Store query metadata and expose metrics.
