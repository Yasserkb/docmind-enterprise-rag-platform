from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.schemas import CreateCollectionRequest
from app.models import Collection
from app.storage.store import store

router = APIRouter(prefix="/collections", tags=["collections"])


@router.post("", response_model=Collection)
def create_collection(req: CreateCollectionRequest) -> Collection:
    return store.add_collection(Collection(**req.model_dump()))


@router.get("", response_model=list[Collection])
def list_collections() -> list[Collection]:
    return list(store.collections.values())


@router.get("/{collection_id}", response_model=Collection)
def get_collection(collection_id: UUID) -> Collection:
    if collection_id not in store.collections:
        raise HTTPException(404, "Collection not found")
    return store.collections[collection_id]


@router.delete("/{collection_id}")
def delete_collection(collection_id: UUID) -> dict:
    if collection_id not in store.collections:
        raise HTTPException(404, "Collection not found")
    del store.collections[collection_id]
    for document_id in [doc.id for doc in store.documents.values() if doc.collection_id == collection_id]:
        del store.documents[document_id]
    for chunk_id in [chunk.id for chunk in store.chunks.values() if chunk.collection_id == collection_id]:
        del store.chunks[chunk_id]
    return {"deleted": str(collection_id)}
