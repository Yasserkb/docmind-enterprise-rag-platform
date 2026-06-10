from app.ingestion.parsers.base import DocumentParser, ParsedDocument

class TxtParser(DocumentParser):
    source_type = "TXT"
    def parse(self, content: bytes, filename: str | None = None) -> ParsedDocument:
        text = content.decode("utf-8", errors="ignore")
        return ParsedDocument(text=text, page_count=max(1, text.count("") + 1), metadata={"filename": filename})
