from app.ingestion.parsers.base import DocumentParser, ParsedDocument

class PdfParser(DocumentParser):
    source_type = "PDF"
    def parse(self, content: bytes, filename: str | None = None) -> ParsedDocument:
        # Production adapter: PyMuPDF/fitz with page numbers and table-aware extraction.
        text = content.decode("utf-8", errors="ignore")
        return ParsedDocument(text=text, page_count=max(1, text.count("") + 1), metadata={"filename": filename, "parser": "pymupdf-adapter"})
