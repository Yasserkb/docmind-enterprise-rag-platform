from app.models import Chunk, SourceCitation


def build_source_citations(results: list[tuple[Chunk, float]]) -> list[SourceCitation]:
    return [
        SourceCitation(
            document_title=chunk.metadata.get("document_title", "Uploaded document"),
            page=chunk.start_page,
            chunk_id=chunk.id,
            chunk_content=chunk.content[:500],
            relevance_score=round(float(score), 4),
        )
        for chunk, score in results
    ]
