# Pylance strict mode
from typing import Any, Literal, List

from pydantic import BaseModel, Field

# --- Request Models ---


class ChunkingStrategyParams(BaseModel):
    """Parameters for a given chunking strategy."""

    chunk_size: int = Field(
        1000, description="Max characters per chunk for fixed_size."
    )
    chunk_overlap: int = Field(100, description="Overlap for fixed_size.")
    min_chunk_size: int = Field(
        50, description="Min characters for paragraph chunking."
    )


class ChunkingStrategy(BaseModel):
    """Defines the chunking strategy to be used."""

    name: Literal["fixed_size", "paragraph"] = Field(
        ..., description="The name of the strategy."
    )
    params: ChunkingStrategyParams = Field(default_factory=ChunkingStrategyParams)  # type: ignore


class DocumentProcessRequest(BaseModel):
    """Request body for the /sync endpoint."""

    document_id: str = Field(..., description="Unique ID for the source document.")
    content: str = Field(..., description="UTF-8 encoded plain text content.")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Arbitrary source metadata."
    )
    chunking_strategy: ChunkingStrategy


# --- Response Models ---


class ChunkValidation(BaseModel):
    """Validation metrics for a chunk."""

    similarity_with_next_chunk: float | None = Field(
        None,
        description="Cosine similarity score with the following chunk. Null for the last chunk.",
    )


class ChunkMetadata(BaseModel):
    """Enriched metadata for a single chunk."""

    parent_document_id: str
    original_metadata: dict[str, Any]
    validation: ChunkValidation


class Chunk(BaseModel):
    """Represents a single processed chunk of text."""

    chunk_id: str
    chunk_index: int
    text: str
    metadata: ChunkMetadata


class ProcessingMetrics(BaseModel):
    """Performance metrics for a processing request."""

    processing_time_ms: int
    total_chunks_produced: int


class DocumentProcessResponse(BaseModel):
    """Success response body for the /sync endpoint."""

    parent_document_id: str
    chunks: list[Chunk]
    metrics: ProcessingMetrics


# --- Error Models ---


class ErrorDetail(BaseModel):
    """Structured error response body."""

    error_code: int
    message: str
    details: dict[str, Any] | str | None = None


# --- Batch Processing Models ---


class BatchProcessRequest(BaseModel):
    """Request body for the /sync-batch endpoint."""
    documents: List[DocumentProcessRequest]


class BatchProcessResponse(BaseModel):
    """Response body for the /sync-batch endpoint."""
    results: List[DocumentProcessResponse]
    total_documents_processed: int