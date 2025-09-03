# Pylance strict mode
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from typing import Any, Dict

from .api_models import DocumentProcessRequest, DocumentProcessResponse, ErrorDetail
from .security import get_api_key

app = FastAPI(
    title="Airbyte Cortex Service",
    description="A service for intelligent, in-flight pre-processing of unstructured data.",
    version="1.0.0",
)

# --- Endpoints ---

@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}

@app.post(
    "/api/v1/sync",
    response_model=DocumentProcessResponse,
    tags=["Processing"],
    responses={
        401: {"model": ErrorDetail},
        500: {"model": ErrorDetail},
    },
)

async def process_document(
    request: DocumentProcessRequest,
    api_key: str = Depends(get_api_key),
) -> Any:
    """
    Processes a single unstructured document, chunks it intelligently,
    and returns AI-ready, semantically coherent chunks.
    """
    # Placeholder for Day 4 logic.
    # We will replace this with a call to the real processing service.
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={
            "error_code": 5001,
            "message": "Processing logic not yet implemented.",
        },
    )