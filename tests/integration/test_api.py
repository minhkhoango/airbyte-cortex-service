# Pylance strict mode
import os
from typing import Any

from fastapi.testclient import TestClient

from cortex_service.main import app

client = TestClient(app)

# Ensure the API key is set for the test environment
API_KEY = os.getenv("CORTEX_API_KEY", "test-key-if-not-set")


def test_health_check() -> None:
    """Tests the /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sync_unauthorized_no_key() -> None:
    """Tests that a request with no API key is rejected."""
    response = client.post("/api/v1/sync", json={})
    assert response.status_code == 401
    assert "missing" in response.json()["detail"].lower()


def test_sync_unauthorized_wrong_key() -> None:
    """Tests that a request with the wrong API key is rejected."""
    headers = {"X-API-Key": "this-is-the-wrong-key"}
    response = client.post("/api/v1/sync", headers=headers, json={})
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_sync_bad_request_payload() -> None:
    """Tests that a malformed request body is rejected with a 422."""
    headers = {"X-API-Key": API_KEY}
    bad_payload: dict[str, Any] = {
        "document_id": "doc123",
        # Missing 'content' and 'chunking_strategy'
    }
    response = client.post("/api/v1/sync", headers=headers, json=bad_payload)
    assert response.status_code == 422  # Unprocessable Entity


def test_sync_e2e_paragraph_chunking_success() -> None:
    """Tests a full, successful request with paragraph chunking."""
    headers = {"X-API-Key": API_KEY}
    payload = {
        "document_id": "doc-xyz-789",
        "content": "This is the first paragraph.\n\nThis is the second.",
        "metadata": {"source": "s3-bucket"},
        "chunking_strategy": {"name": "paragraph", "params": {"min_chunk_size": 10}},
    }
    response = client.post("/api/v1/sync", headers=headers, json=payload)
    response_data = response.json()

    assert response.status_code == 200
    assert response_data["parent_document_id"] == "doc-xyz-789"
    assert len(response_data["chunks"]) == 2
    assert response_data["chunks"][0]["text"] == "This is the first paragraph."
    assert response_data["metrics"]["total_chunks_produced"] == 2
    assert (
        "similarity_with_next_chunk"
        in response_data["chunks"][0]["metadata"]["validation"]
    )
