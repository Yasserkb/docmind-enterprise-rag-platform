import hashlib
from datetime import datetime

from app.ingestion.chunking import EmbeddingService, create_chunker, select_strategy
from app.ingestion.parsers.registry import PARSERS
from app.models import Chunk, Collection, Document, DocumentStatus, SourceType
from app.observability.metrics import DOCUMENTS_INDEXED
from app.storage.store import Store


def parse_content(source_type: SourceType, content: bytes, filename: str | None = None):
    parser = PARSERS.get(source_type, PARSERS[SourceType.TXT])
    return parser.parse(content, filename)


class IngestionPipeline:
    """Application service responsible for document ingestion.

    The class deliberately orchestrates the ingestion flow without coupling the rest of the
    application to a concrete parser, embedding provider, vector database, or search engine.
    """

    def __init__(self, store: Store):
        self.store = store
        self.embeddings = EmbeddingService()

    def ingest_bytes(
        self,
        collection: Collection,
        filename: str,
        source_type: SourceType,
        content: bytes,
        metadata: dict | None = None,
    ) -> Document:
        metadata = metadata or {}
        content_hash = hashlib.sha256(content).hexdigest()
        existing = next((doc for doc in self.store.documents.values() if doc.content_hash == content_hash), None)
        if existing:
            return existing

        document = Document(
            title=filename,
            collection_id=collection.id,
            source_type=source_type,
            source_uri=filename,
            content_hash=content_hash,
            status=DocumentStatus.PROCESSING,
            metadata=metadata,
        )
        self.store.documents[document.id] = document

        try:
            parsed = parse_content(source_type, content, filename)
            document.page_count = parsed.page_count
            document.metadata = {**document.metadata, **(parsed.metadata or {})}

            strategy = collection.chunking_strategy if collection.chunking_strategy in {
                "fixed",
                "recursive",
                "semantic",
                "structural",
            } else select_strategy(document)
            pieces = create_chunker(strategy)(parsed.text)
            vectors = self.embeddings.embed_batch([piece.content for piece in pieces])

            chunks = [
                Chunk(
                    document_id=document.id,
                    collection_id=collection.id,
                    content=piece.content,
                    chunk_index=index,
                    token_count=piece.token_count,
                    start_page=piece.start_page,
                    end_page=piece.end_page,
                    heading_path=piece.heading_path,
                    metadata={**(piece.metadata or {}), "document_title": filename},
                    embedding=vectors[index],
                )
                for index, piece in enumerate(pieces)
            ]
            self.store.add_chunks(chunks)
            document.status = DocumentStatus.INDEXED
            document.indexed_at = datetime.utcnow()
            DOCUMENTS_INDEXED.labels(collection=str(collection.id), source_type=source_type.value).inc()
        except Exception as exc:  # pragma: no cover - defensive status mapping
            document.status = DocumentStatus.FAILED
            document.error_message = str(exc)
        return document
