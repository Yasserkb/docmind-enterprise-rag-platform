import re
from app.ingestion.parsers.base import DocumentParser, ParsedDocument

class HtmlParser(DocumentParser):
    source_type = "HTML"
    def parse(self, content: bytes, filename: str | None = None) -> ParsedDocument:
        raw = content.decode("utf-8", errors="ignore")
        text = re.sub(r"<[^>]+>", " ", raw)
        text = re.sub(r"\s+", " ", text).strip()
        return ParsedDocument(text=text, page_count=1, metadata={"filename": filename, "parser": "beautifulsoup-trafilatura-adapter"})
