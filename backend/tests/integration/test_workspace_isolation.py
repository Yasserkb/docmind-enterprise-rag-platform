from fastapi.testclient import TestClient

from app.main import app
from app.storage.store import store


def test_workspace_cannot_list_or_query_another_workspace_collection() -> None:
    store.collections.clear()
    store.documents.clear()
    store.chunks.clear()
    client = TestClient(app)
    alpha = {"X-Workspace-Id": "alpha", "X-User-Id": "alice"}
    beta = {"X-Workspace-Id": "beta", "X-User-Id": "bob"}

    created = client.post("/api/v1/collections", json={"name": "Alpha private"}, headers=alpha)
    assert created.status_code == 200
    collection_id = created.json()["id"]

    assert [item["id"] for item in client.get("/api/v1/collections", headers=alpha).json()] == [collection_id]
    assert client.get("/api/v1/collections", headers=beta).json() == []
    assert client.get(f"/api/v1/collections/{collection_id}", headers=beta).status_code == 404
    assert client.post(
        "/api/v1/query",
        json={"question": "Reveal Alpha data", "collection_id": collection_id},
        headers=beta,
    ).status_code == 404


def test_invalid_local_role_is_rejected() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/collections", headers={"X-User-Role": "superuser"})
    assert response.status_code == 400
