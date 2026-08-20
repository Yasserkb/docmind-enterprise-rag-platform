from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas import CreateCollectionRequest
from app.models import Collection
from app.core.security import RequestIdentity, current_identity
from app.storage.store import store

router = APIRouter(prefix="/collections", tags=["collections"])


@router.post("", response_model=Collection)
def create_collection(req: CreateCollectionRequest, identity: RequestIdentity = Depends(current_identity)) -> Collection:
    return store.add_collection(Collection(**req.model_dump(), workspace_id=identity.workspace_id, created_by=identity.user_id))


@router.get("", response_model=list[Collection])
def list_collections(identity: RequestIdentity = Depends(current_identity)) -> list[Collection]:
    return [item for item in store.collections.values() if item.workspace_id == identity.workspace_id]


@router.get("/{collection_id}", response_model=Collection)
def get_collection(collection_id: UUID, identity: RequestIdentity = Depends(current_identity)) -> Collection:
    collection = store.collections.get(collection_id)
    if not collection or collection.workspace_id != identity.workspace_id:
        raise HTTPException(404, "Collection not found")
    return collection


@router.delete("/{collection_id}")
def delete_collection(collection_id: UUID, identity: RequestIdentity = Depends(current_identity)) -> dict:
    collection = store.collections.get(collection_id)
    if not collection or collection.workspace_id != identity.workspace_id:
        raise HTTPException(404, "Collection not found")
    del store.collections[collection_id]
    for document_id in [doc.id for doc in store.documents.values() if doc.collection_id == collection_id]:
        del store.documents[document_id]
    for chunk_id in [chunk.id for chunk in store.chunks.values() if chunk.collection_id == collection_id]:
        del store.chunks[chunk_id]
    return {"deleted": str(collection_id)}
