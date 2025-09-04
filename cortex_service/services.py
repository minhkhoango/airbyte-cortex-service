# Pylance strict mode
import time
import uuid

from . import chunking, validation
from .api_models import (
    BatchProcessRequest,
    BatchProcessResponse,
    Chunk,
    ChunkMetadata,
    ChunkValidation,
    DocumentProcessRequest,
    DocumentProcessResponse,
    ProcessingMetrics,
)


def process_document_logic(request: DocumentProcessRequest) -> DocumentProcessResponse:
    """
    Orchestrates the document processing workflow.
    Selects chunking strategy, performs chunking, validates, and formats the response.
    """
    start_time = time.monotonic()

    # 1. Select and execute chunking strategy
    strategy = request.chunking_strategy
    if strategy.name == "paragraph":
        chunks_text = chunking.chunk_by_paragraph(
            request.content, strategy.params.min_chunk_size
        )
    elif strategy.name == "fixed_size":
        chunks_text = chunking.chunk_by_fixed_size(
            request.content, strategy.params.chunk_size, strategy.params.chunk_overlap
        )
    else:
        # This case should ideally be caught by Pydantic, but defensive coding is good.
        raise ValueError(f"Unknown chunking strategy: {strategy.name}")

    # 2. Perform semantic validation
    similarities = validation.calculate_semantic_similarity(chunks_text)

    # 3. Format the response chunks
    response_chunks: list[Chunk] = []
    for i, text in enumerate(chunks_text):
        chunk = Chunk(
            chunk_id=str(uuid.uuid4()),
            chunk_index=i,
            text=text,
            metadata=ChunkMetadata(
                parent_document_id=request.document_id,
                original_metadata=request.metadata,
                validation=ChunkValidation(similarity_with_next_chunk=similarities[i]),
            ),
        )
        response_chunks.append(chunk)

    end_time = time.monotonic()
    processing_time_ms = int((end_time - start_time) * 1000)

    return DocumentProcessResponse(
        parent_document_id=request.document_id,
        chunks=response_chunks,
        metrics=ProcessingMetrics(
            processing_time_ms=processing_time_ms,
            total_chunks_produced=len(response_chunks),
        ),
    )


def process_documents_batch_logic(request: BatchProcessRequest) -> BatchProcessResponse:
    """Orchestrates the batch processing of multiple documents."""
    results: list[DocumentProcessResponse] = []
    for doc in request.documents:
        # For the MVP, we process sequentially.
        # A future optimization could use asyncio for concurrent processing.
        result = process_document_logic(doc)
        results.append(result)

    return BatchProcessResponse(results=results, total_documents_processed=len(results))
