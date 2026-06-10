from dataclasses import dataclass


@dataclass(frozen=True)
class ChunkConfig:
    strategy: str
    chunk_size: int = 512
    overlap: int = 64
    similarity_threshold: float = 0.70
    max_chunk_size: int = 1024
    respect_headings: bool = False
    respect_tables: bool = False


@dataclass
class ChunkPiece:
    content: str
    token_count: int
    start_page: int = 1
    end_page: int = 1
    heading_path: str | None = None
    metadata: dict | None = None


def tokens(text: str) -> list[str]:
    return [t for t in text.replace("\n", " ").split(" ") if t]
