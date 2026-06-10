from fastapi.testclient import TestClient

from app.main import app


def test_demo_seed_api_flow():
    client = TestClient(app)
    response = client.post("/api/v1/demo/seed")
    assert response.status_code == 200
    assert response.json()["collection_id"]
    assert client.get("/api/v1/collections").status_code == 200
