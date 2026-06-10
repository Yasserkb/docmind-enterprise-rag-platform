from app.ingestion.chunking.base import ChunkConfig, ChunkPiece, tokens


def recursive_chunk(text: str, cfg: ChunkConfig = ChunkConfig("recursive")) -> list[ChunkPiece]:
    parts = [part.strip() for part in text.split("\n\n") if part.strip()] or [text]
    chunks: list[ChunkPiece] = []
    current: list[str] = []
    count = 0
    for part in parts:
        part_tokens = len(tokens(part))
        if current and count + part_tokens > cfg.chunk_size:
            content = "\n\n".join(current)
            chunks.append(ChunkPiece(content, len(tokens(content)), metadata={"strategy": "recursive"}))
            overlap_text = " ".join(tokens(content)[-cfg.overlap :])
            current = [overlap_text] if overlap_text else []
            count = len(tokens(overlap_text))
        current.append(part)
        count += part_tokens
    if current:
        content = "\n\n".join(current)
        chunks.append(ChunkPiece(content, len(tokens(content)), metadata={"strategy": "recursive"}))
    return chunks
