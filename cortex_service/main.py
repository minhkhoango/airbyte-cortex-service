# Pylance strict mode
from typing import Any

from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from . import services
from .api_models import DocumentProcessRequest, DocumentProcessResponse, ErrorDetail
from .loggin_config import configure_logging
from .security import get_api_key

configure_logging()

app = FastAPI(
    title="Airbyte Cortex Service",
    description="A service for intelligent, in-flight pre-processing of unstructured data.",
    version="1.0.0",
)

# Add this line to expose the /metrics endpoint
Instrumentator().instrument(app).expose(app)

# --- Endpoints ---


@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}


@app.post(
    "/api/v1/sync",
    response_model=DocumentProcessResponse,
    tags=["Processing"],
    responses={
        401: {"model": ErrorDetail},
        422: {"model": ErrorDetail},
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
    try:
        response = services.process_document_logic(request)
        return response
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": 5000,
                "message": "An internal error occurred during processing.",
                "details": str(e),
            },
        )
