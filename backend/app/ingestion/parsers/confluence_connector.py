from app.ingestion.parsers.base import ParsedDocument

class ConfluenceConnector:
    """Production adapter boundary for Confluence REST API page-tree traversal."""
    def fetch_page(self, page_id: str) -> ParsedDocument:
        return ParsedDocument(text=f"Confluence connector placeholder for page {page_id}", page_count=1, metadata={"page_id": page_id})
