

# Pylance strict mode
from typing import List
from unstructured.partition.text import partition_text

def chunk_by_paragraph(text: str, min_chunk_size: int) -> List[str]:
    """Chunks text by paragraph, filtering for a minimum size."""
    elements = partition_text(text=text)
    raw_chunks = [str(el) for el in elements]
    return [chunk for chunk in raw_chunks if len(chunk) >= min_chunk_size]

def chunk_by_fixed_size(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    """Chunks text by a fixed character size with overlap."""
    # This is a naive implementation for the MVP.
    # More robust libraries like LangChain's text_splitter could be used post-MVP.
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")
    
    chunks: List[str] = []
    for i in range(0, len(text), chunk_size - chunk_overlap):
        chunk = text[i:i + chunk_size]
        if chunk:
            chunks.append(chunk)
    return chunks