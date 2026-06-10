from app.models import Chunk
from app.retrieval.elasticsearch_client import tokenize


class CrossEncoderReranker:
    """Deterministic reranker adapter.

    In production, this adapter can call a cross-encoder model such as
    `cross-encoder/ms-marco-MiniLM-L-6-v2` without changing the RAG pipeline.
    """

    def score(self, question: str, chunk: Chunk) -> float:
        question_terms = {term for term in tokenize(question) if len(term) > 2}
        chunk_terms = {term for term in tokenize(chunk.content) if len(term) > 2}
        if not question_terms:
            return 0.0
        lexical_overlap = len(question_terms & chunk_terms) / len(question_terms)
        length_prior = min(1.0, 350 / max(50, len(chunk.content)))
        return round(0.75 * lexical_overlap + 0.25 * length_prior, 4)

    def rerank(self, question: str, chunks: list[Chunk]) -> list[tuple[Chunk, float]]:
        return sorted([(chunk, self.score(question, chunk)) for chunk in chunks], key=lambda item: item[1], reverse=True)
