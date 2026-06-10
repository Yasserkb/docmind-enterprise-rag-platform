from __future__ import annotations
from dataclasses import dataclass

@dataclass
class ParsedDocument:
    text: str
    page_count: int = 1
    metadata: dict | None = None

class DocumentParser:
    source_type = "TXT"
    def parse(self, content: bytes, filename: str | None = None) -> ParsedDocument:
        return ParsedDocument(content.decode("utf-8", errors="ignore"), 1, {"filename": filename})
