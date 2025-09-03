# Pylance strict mode
from typing import cast

import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore

# Load the model once at startup. This is a critical optimization.
# In a real production system, this would be managed more carefully.
MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(chunks: list[str]) -> list[float | None]:
    """
    Calculates the cosine similarity between adjacent chunks.
    The last chunk will have a similarity of None.
    """
    if len(chunks) < 2:
        return [None] * len(chunks)

    embeddings = MODEL.encode(chunks, convert_to_numpy=True)

    similarities: list[float | None] = []
    for i in range(len(chunks) - 1):
        embedding_current: NDArray[np.float64] = embeddings[i].reshape(1, -1)
        embedding_next: NDArray[np.float64] = embeddings[i + 1].reshape(1, -1)

        # Use cast to handle sklearn's type ambiguity
        similarity_score_array: NDArray[np.float64] = cast(
            NDArray[np.float64], cosine_similarity(embedding_current, embedding_next)
        )

        # Extract the similarity score safely
        similarity_score: float = float(similarity_score_array[0, 0])
        similarities.append(similarity_score)

    similarities.append(None)  # Last chunk has no next chunk to compare to
    return similarities
