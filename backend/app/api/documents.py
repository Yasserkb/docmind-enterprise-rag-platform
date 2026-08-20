from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from app.api.schemas import IngestS3Request, IngestUrlRequest
from app.ingestion.pipeline import IngestionPipeline
from app.models import Document, SourceType
from app.core.security import RequestIdentity, current_identity
from app.storage.store import store

router = APIRouter(tags=["documents"])


@router.post("/collections/{collection_id}/documents", response_model=Document)
async def upload_document(
    collection_id: UUID,
    file: UploadFile = File(...),
    source_type: SourceType = Form(SourceType.TXT),
    identity: RequestIdentity = Depends(current_identity),
) -> Document:
    collection = store.collections.get(collection_id)
    if not collection or collection.workspace_id != identity.workspace_id:
        raise HTTPException(404, "Collection not found")
    return IngestionPipeline(store).ingest_bytes(
        collection,
        file.filename or "uploaded",
        source_type,
        await file.read(),
        {"document_title": file.filename}, identity.user_id,
    )


@router.post("/collections/{collection_id}/ingest/url", response_model=Document)
def ingest_url(collection_id: UUID, req: IngestUrlRequest, identity: RequestIdentity = Depends(current_identity)) -> Document:
    collection = store.collections.get(collection_id)
    if not collection or collection.workspace_id != identity.workspace_id:
        raise HTTPException(404, "Collection not found")
    content = f"URL connector placeholder for {req.url}. Replace with trafilatura or BeautifulSoup extraction in production.".encode()
    return IngestionPipeline(store).ingest_bytes(collection, req.url, SourceType.URL, content, {"source_url": req.url, **req.metadata}, identity.user_id)


@router.post("/collections/{collection_id}/ingest/s3", response_model=Document)
def ingest_s3(collection_id: UUID, req: IngestS3Request, identity: RequestIdentity = Depends(current_identity)) -> Document:
    collection = store.collections.get(collection_id)
    if not collection or collection.workspace_id != identity.workspace_id:
        raise HTTPException(404, "Collection not found")
    uri = f"s3://{req.bucket}/{req.key}"
    return IngestionPipeline(store).ingest_bytes(collection, uri, SourceType.S3, f"S3 connector placeholder for {uri}".encode(), {"source_s3": uri, **req.metadata}, identity.user_id)


@router.get("/collections/{collection_id}/documents", response_model=list[Document])
def list_documents(collection_id: UUID, identity: RequestIdentity = Depends(current_identity)) -> list[Document]:
    collection = store.collections.get(collection_id)
    if not collection or collection.workspace_id != identity.workspace_id:
        raise HTTPException(404, "Collection not found")
    return [document for document in store.documents.values() if document.collection_id == collection_id and document.workspace_id == identity.workspace_id]


@router.get("/documents/{document_id}", response_model=Document)
def get_document(document_id: UUID, identity: RequestIdentity = Depends(current_identity)) -> Document:
    document = store.documents.get(document_id)
    if not document or document.workspace_id != identity.workspace_id or (document.allowed_user_ids and identity.user_id not in document.allowed_user_ids):
        raise HTTPException(404, "Document not found")
    return document


@router.delete("/documents/{document_id}")
def delete_document(document_id: UUID, identity: RequestIdentity = Depends(current_identity)) -> dict:
    document = store.documents.get(document_id)
    if not document or document.workspace_id != identity.workspace_id:
        raise HTTPException(404, "Document not found")
    del store.documents[document_id]
    for chunk_id in [chunk.id for chunk in store.chunks.values() if chunk.document_id == document_id]:
        del store.chunks[chunk_id]
    return {"deleted": str(document_id)}
