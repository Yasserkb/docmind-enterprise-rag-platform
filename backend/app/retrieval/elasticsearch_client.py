import math
from collections import Counter
from uuid import UUID

from app.models import Chunk


def tokenize(text: str) -> list[str]:
    return [term.strip(".,;:!?()[]{}\"'").lower() for term in text.split() if term.strip()]


class KeywordSearchClient:
    """BM25-style keyword search adapter with an Elasticsearch-compatible boundary."""

    def search(self, query: str, collection_id: UUID, chunks: list[Chunk], top_k: int = 20) -> list[tuple[Chunk, float]]:
        query_terms = tokenize(query)
        docs = [chunk for chunk in chunks if chunk.collection_id == collection_id]
        if not query_terms or not docs:
            return []

        avgdl = sum(len(tokenize(chunk.content)) for chunk in docs) / len(docs)
        document_frequencies: Counter[str] = Counter()
        chunk_term_frequencies: dict[str, Counter[str]] = {}

        for chunk in docs:
            terms = Counter(tokenize(chunk.content))
            chunk_term_frequencies[str(chunk.id)] = terms
            for term in set(terms):
                document_frequencies[term] += 1

        k1 = 1.5
        b = 0.75
        scored: list[tuple[Chunk, float]] = []
        for chunk in docs:
            score = 0.0
            terms = chunk_term_frequencies[str(chunk.id)]
            document_length = sum(terms.values()) or 1
            for term in query_terms:
                term_frequency = terms[term]
                if not term_frequency:
                    continue
                idf = math.log(1 + (len(docs) - document_frequencies[term] + 0.5) / (document_frequencies[term] + 0.5))
                score += idf * (term_frequency * (k1 + 1)) / (
                    term_frequency + k1 * (1 - b + b * document_length / avgdl)
                )
            if score > 0:
                scored.append((chunk, score))
        return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]
