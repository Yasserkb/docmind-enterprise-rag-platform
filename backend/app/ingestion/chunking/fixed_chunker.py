from app.ingestion.chunking.base import ChunkConfig, ChunkPiece, tokens


def fixed_chunk(text: str, cfg: ChunkConfig = ChunkConfig("fixed")) -> list[ChunkPiece]:
    words = tokens(text)
    step = max(1, cfg.chunk_size - cfg.overlap)
    chunks = []
    for i in range(0, len(words), step):
        window = words[i : i + cfg.chunk_size]
        if window:
            chunks.append(ChunkPiece(" ".join(window), len(window), metadata={"strategy": "fixed"}))
    return chunks
