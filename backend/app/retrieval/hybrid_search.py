from uuid import UUID

from app.models import Chunk
from app.retrieval.elasticsearch_client import KeywordSearchClient
from app.retrieval.qdrant_client import SemanticSearchClient
from app.retrieval.reranker import CrossEncoderReranker
from app.retrieval.result_fusion import reciprocal_rank_fusion


class HybridSearchEngine:
    def __init__(self):
        self.semantic = SemanticSearchClient()
        self.keyword = KeywordSearchClient()
        self.reranker = CrossEncoderReranker()

    def expand_query(self, question: str) -> list[str]:
        normalized = question.strip()
        return [normalized, normalized.replace("?", ""), f"information about {normalized}"]

    def hyde_document(self, question: str) -> str:
        return f"This document contains the answer to the question: {question}"

    def search(
        self,
        question: str,
        collection_id: UUID,
        chunks: list[Chunk],
        top_k: int = 5,
        use_hyde: bool = True,
        rerank: bool = True,
    ) -> list[tuple[Chunk, float]]:
        queries = self.expand_query(question)
        if use_hyde:
            queries.append(self.hyde_document(question))

        result_sets: list[list[tuple[Chunk, float]]] = []
        for query in queries:
            result_sets.append(self.semantic.search(query, collection_id, chunks, top_k=20))
            result_sets.append(self.keyword.search(query, collection_id, chunks, top_k=20))

        merged_chunks, rrf_scores = reciprocal_rank_fusion(result_sets)
        candidate_chunks = merged_chunks[:20]
        if rerank:
            reranked = self.reranker.rerank(question, candidate_chunks)
            return [(chunk, max(score, rrf_scores.get(str(chunk.id), 0.0))) for chunk, score in reranked if score >= 0.05][:top_k]
        return [(chunk, rrf_scores[str(chunk.id)]) for chunk in candidate_chunks[:top_k]]
