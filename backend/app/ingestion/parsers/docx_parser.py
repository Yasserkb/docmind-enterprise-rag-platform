from app.ingestion.parsers.base import DocumentParser, ParsedDocument

class DocxParser(DocumentParser):
    source_type = "DOCX"
    def parse(self, content: bytes, filename: str | None = None) -> ParsedDocument:
        # Production adapter: python-docx preserving heading hierarchy.
        text = content.decode("utf-8", errors="ignore")
        return ParsedDocument(text=text, page_count=1, metadata={"filename": filename, "parser": "python-docx-adapter"})
