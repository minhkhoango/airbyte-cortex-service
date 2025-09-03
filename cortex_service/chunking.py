# Pylance strict mode

from unstructured.partition.text import partition_text


def chunk_by_paragraph(text: str, min_chunk_size: int) -> list[str]:
    """Chunks text by paragraph, filtering for a minimum size."""
    elements = partition_text(text=text)
    raw_chunks = [str(el) for el in elements]
    return [chunk for chunk in raw_chunks if len(chunk) >= min_chunk_size]


def chunk_by_fixed_size(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Chunks text by a fixed character size with overlap."""
    # This is a naive implementation for the MVP.
    # More robust libraries like LangChain's text_splitter could be used post-MVP.
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    if not text:
        return []

    chunks: list[str] = []

    # Calculate the step size for moving through the text
    step_size = chunk_size - chunk_overlap

    # When step_size <= 0 (overlap >= chunk_size), move by 1 to avoid infinite loops
    if step_size <= 0:
        step_size = 1

    i = 0
    while i < len(text):
        # Create chunk from current position
        chunk = text[i : i + chunk_size]
        chunks.append(chunk)

        # Move to next position
        i += step_size

    return chunks
