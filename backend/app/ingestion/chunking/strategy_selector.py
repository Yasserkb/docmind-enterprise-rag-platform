from app.models import Document, SourceType


def select_strategy(document: Document) -> str:
    if document.source_type in {SourceType.PDF, SourceType.DOCX} and document.page_count > 50:
        return "structural"
    if document.metadata.get("type") == "contract":
        return "structural"
    if document.language != "en":
        return "recursive"
    return "semantic"
