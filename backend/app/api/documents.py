from uuid import UUID

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.api.schemas import IngestS3Request, IngestUrlRequest
from app.ingestion.pipeline import IngestionPipeline
from app.models import Document, SourceType
from app.storage.store import store

router = APIRouter(tags=["documents"])


@router.post("/collections/{collection_id}/documents", response_model=Document)
async def upload_document(
    collection_id: UUID,
    file: UploadFile = File(...),
    source_type: SourceType = Form(SourceType.TXT),
) -> Document:
    collection = store.collections.get(collection_id)
    if not collection:
        raise HTTPException(404, "Collection not found")
    return IngestionPipeline(store).ingest_bytes(
        collection,
        file.filename or "uploaded",
        source_type,
        await file.read(),
        {"document_title": file.filename},
    )


@router.post("/collections/{collection_id}/ingest/url", response_model=Document)
def ingest_url(collection_id: UUID, req: IngestUrlRequest) -> Document:
    collection = store.collections.get(collection_id)
    if not collection:
        raise HTTPException(404, "Collection not found")
    content = f"URL connector placeholder for {req.url}. Replace with trafilatura or BeautifulSoup extraction in production.".encode()
    return IngestionPipeline(store).ingest_bytes(collection, req.url, SourceType.URL, content, {"source_url": req.url, **req.metadata})


@router.post("/collections/{collection_id}/ingest/s3", response_model=Document)
def ingest_s3(collection_id: UUID, req: IngestS3Request) -> Document:
    collection = store.collections.get(collection_id)
    if not collection:
        raise HTTPException(404, "Collection not found")
    uri = f"s3://{req.bucket}/{req.key}"
    return IngestionPipeline(store).ingest_bytes(collection, uri, SourceType.S3, f"S3 connector placeholder for {uri}".encode(), {"source_s3": uri, **req.metadata})


@router.get("/collections/{collection_id}/documents", response_model=list[Document])
def list_documents(collection_id: UUID) -> list[Document]:
    return [document for document in store.documents.values() if document.collection_id == collection_id]


@router.get("/documents/{document_id}", response_model=Document)
def get_document(document_id: UUID) -> Document:
    if document_id not in store.documents:
        raise HTTPException(404, "Document not found")
    return store.documents[document_id]


@router.delete("/documents/{document_id}")
def delete_document(document_id: UUID) -> dict:
    if document_id not in store.documents:
        raise HTTPException(404, "Document not found")
    del store.documents[document_id]
    for chunk_id in [chunk.id for chunk in store.chunks.values() if chunk.document_id == document_id]:
        del store.chunks[chunk_id]
    return {"deleted": str(document_id)}
