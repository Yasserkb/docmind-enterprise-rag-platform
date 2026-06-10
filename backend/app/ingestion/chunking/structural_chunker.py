import re

from app.ingestion.chunking.base import ChunkConfig, ChunkPiece, tokens


def structural_chunk(
    text: str,
    cfg: ChunkConfig = ChunkConfig("structural", max_chunk_size=1024, respect_headings=True, respect_tables=True),
) -> list[ChunkPiece]:
    blocks = re.split(r"(?=^#{1,6}\s+|^[A-Z][A-Z0-9 .-]{6,}$)", text, flags=re.M)
    chunks: list[ChunkPiece] = []
    heading: str | None = None

    for block in [x.strip() for x in blocks if x.strip()]:
        first_line = block.splitlines()[0] if block.splitlines() else ""
        if first_line.startswith("#") or first_line.isupper():
            heading = first_line.lstrip("# ").strip()
        words = tokens(block)
        for i in range(0, len(words), cfg.max_chunk_size):
            content = " ".join(words[i : i + cfg.max_chunk_size])
            if content:
                chunks.append(
                    ChunkPiece(
                        content=content,
                        token_count=len(tokens(content)),
                        heading_path=heading,
                        metadata={"strategy": "structural", "preserves_structure": True},
                    )
                )
    return chunks
