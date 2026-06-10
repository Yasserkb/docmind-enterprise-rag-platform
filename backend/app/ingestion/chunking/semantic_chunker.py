import re

from app.ingestion.chunking.base import ChunkConfig, ChunkPiece, tokens
from app.ingestion.embeddings import EmbeddingService, cosine


def semantic_chunk(text: str, cfg: ChunkConfig = ChunkConfig("semantic")) -> list[ChunkPiece]:
    embedder = EmbeddingService()
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    if not sentences:
        return []

    chunks: list[str] = []
    current = [sentences[0]]
    previous_embedding = embedder.embed(sentences[0])

    for sentence in sentences[1:]:
        current_embedding = embedder.embed(sentence)
        candidate = " ".join(current + [sentence])
        if len(tokens(candidate)) > cfg.chunk_size or cosine(previous_embedding, current_embedding) < cfg.similarity_threshold:
            chunks.append(" ".join(current))
            current = [sentence]
        else:
            current.append(sentence)
        previous_embedding = current_embedding

    chunks.append(" ".join(current))
    return [ChunkPiece(chunk, len(tokens(chunk)), metadata={"strategy": "semantic"}) for chunk in chunks]
