# scripts/client.py
# Pylance strict mode

import json
import os
from typing import Any, cast

import requests
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables (like CORTEX_API_KEY) from the .env file
load_dotenv()
CORTEX_API_URL = "http://127.0.0.1:8000/api/v1/sync"
API_KEY = os.getenv("CORTEX_API_KEY")

# --- Sample Data ---
# A sample of technical documentation that would be difficult to chunk naively
SAMPLE_TECHNICAL_DOC = """
A Dockerfile is a text document that contains all the commands a user could
call on the command line to assemble an image.

# Stage 1: Build stage
FROM python:3.11-slim as builder
WORKDIR /app
ENV POETRY_NO_INTERACTION=1
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --no-dev

# Stage 2: Final stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/.venv /.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY ./cortex_service ./cortex_service
CMD ["uvicorn", "cortex_service.main:app", "--host", "0.0.0.0", "--port", "8000"]

Using multi-stage builds allows you to drastically reduce your final image
size, separating build-time dependencies from runtime dependencies.
"""


def run_sync_simulation() -> None:
    """
    Simulates an Airbyte sync by sending a document to the Cortex service
    and printing the resulting stream of chunked records.
    """

    print("--- Starting Cortex Sync Simulation ---")

    if not API_KEY:
        print("Error: CORTEX_API_KEY not found in .env file. Aborting.")
        return

    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY,
    }

    payload: dict[str, Any] = {
        "document_id": "doc-dockerfile-best-practice-001",
        "content": SAMPLE_TECHNICAL_DOC,
        "metadata": {"source_file": "docs/deployment.md", "author": "admin"},
        "chunking_strategy": {"name": "paragraph", "params": {"min_chunk_size": 30}},
    }

    print(f"\n[1] Sending document '{payload['document_id']}' to Cortex service...")

    try:
        response = requests.post(
            CORTEX_API_URL, headers=headers, json=payload, timeout=30
        )
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"\n[!] API Request Failed: {e}")
        return

    print(f"[2] Received successful response (Status {response.status_code})")

    response_data: dict[str, Any] = response.json()
    chunks: list[dict[str, Any]] = cast(
        list[dict[str, Any]], response_data.get("chunks", [])
    )
    metrics: dict[str, Any] = cast(dict[str, Any], response_data.get("metrics", {}))

    print("\n--- Emitting AirbyteRecordMessages (Simulated) ---")
    print(f"Total Chunks Produced: {metrics.get('total_chunks_produced', 'N/A')}")
    print(f"Processing Time: {metrics.get('processing_time_ms', 'N/A')}ms")
    print("-" * 50)

    for chunk in chunks:
        # Simulating the Airbyte message format
        airbyte_message = {"type": "RECORD", "record": {"data": chunk}}
        print(json.dumps(airbyte_message, indent=2))
        print("-" * 50)

    print("--- Sync Simulation Complete ---")


if __name__ == "__main__":
    run_sync_simulation()
