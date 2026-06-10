from app.ingestion.chunking.base import ChunkConfig, ChunkPiece, tokens
from app.ingestion.chunking.fixed_chunker import fixed_chunk
from app.ingestion.chunking.recursive_chunker import recursive_chunk
from app.ingestion.chunking.semantic_chunker import semantic_chunk
from app.ingestion.chunking.strategy_selector import select_strategy
from app.ingestion.chunking.structural_chunker import structural_chunk
from app.ingestion.embeddings import EmbeddingService, cosine


def create_chunker(strategy: str):
    return {
        "fixed": fixed_chunk,
        "recursive": recursive_chunk,
        "semantic": semantic_chunk,
        "structural": structural_chunk,
    }.get(strategy, semantic_chunk)


__all__ = [
    "ChunkConfig",
    "ChunkPiece",
    "EmbeddingService",
    "cosine",
    "create_chunker",
    "fixed_chunk",
    "recursive_chunk",
    "semantic_chunk",
    "select_strategy",
    "structural_chunk",
    "tokens",
]
