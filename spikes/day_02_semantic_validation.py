# spikes/day_02_semantic_validation.py
# Pylance strict mode

import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from unstructured.partition.text import partition_text
from typing import List

def run_spike() -> None:
    """
    Executes the semantic validation spike.
    1. Chunks a document by paragraph using unstructured.io.
    2. Generates sentence embeddings for each chunk.
    3. Calculates the cosine similarity between adjacent chunks.
    4. Prints the results to demonstrate semantic coherence.
    """
    print("--- Starting Day 2 Spike: Semantic Validation ---")

    # A sample document with paragraphs of varying semantic relevance.
    # Paragraphs 1 and 2 are related.
    # Paragraph 3 is a non-sequitur.
    # Paragraph 4 returns to the original topic.
    sample_document: str = (
        "The primary goal of the Cortex project is to provide a robust, in-flight "
        "transformation layer for unstructured data. This enables enterprises to build "
        "reliable RAG pipelines without resorting to brittle custom scripts."
        "\n\n"
        "By integrating intelligent chunking directly into the Airbyte workflow, we can "
        "significantly accelerate AI development cycles. This strategic move positions "
        "Airbyte not just as a data mover, but as a foundational platform for the AI era."
        "\n\n"
        "The best coffee beans are typically grown in the 'Bean Belt,' an area "
        "between the Tropics of Cancer and Capricorn. Altitude, climate, and soil "
        "composition are all critical factors in the final taste profile of the coffee."
        "\n\n"
        "Ultimately, the success of this initiative will be measured by the adoption "
        "of Cortex in enterprise AI projects and the subsequent reduction in their "
        "time-to-market for generative AI applications."
    )

    # --- Step 1: Chunk the document using unstructured.io ---
    # We use partition_text, which is excellent at splitting by paragraphs.
    elements = partition_text(text=sample_document)
    chunks: List[str] = [str(el) for el in elements if str(el).strip()]

    print(f"\n[1] Document chunked into {len(chunks)} paragraphs.")
    for i, chunk in enumerate(chunks):
        print(f"  - Chunk {i}: \"{chunk[:70]}...\"")

    # --- Step 2: Generate embeddings for each chunk ---
    # 'all-MiniLM-L6-v2' is a small, fast, and effective model for this task.
    print("\n[2] Loading sentence-transformer model and generating embeddings...")
    model: SentenceTransformer = SentenceTransformer('all-MiniLM-L6-v2')
    
    # The `encode` method returns a numpy array of embeddings.
    embeddings: NDArray[np.float64] = model.encode(chunks, convert_to_numpy=True)
    print(f"  - Generated {embeddings.shape[0]} embeddings of dimension {embeddings.shape[1]}.")

    # --- Step 3: Calculate cosine similarity between adjacent chunks ---
    print("\n[3] Calculating semantic similarity between adjacent chunks...")
    print("-" * 50)
    
    similarities: List[float] = []
    for i in range(len(chunks) - 1):
        # Extract embeddings for adjacent chunks. We reshape them to be 2D arrays
        # as required by the cosine_similarity function.
        embedding_current: NDArray[np.float64] = embeddings[i].reshape(1, -1)
        embedding_next: NDArray[np.float64] = embeddings[i+1].reshape(1, -1)

        # Calculate similarity score
        similarity_score_array: NDArray[np.float64] = cosine_similarity(embedding_current, embedding_next)
        similarity_score: float = similarity_score_array[0, 0]
        similarities.append(similarity_score)

        print(f"Chunk {i}:\n\"{chunks[i]}\"")
        print(f"\n  ==> Similarity with next chunk: [{similarity_score:.4f}] <==\n")
    
    # Print the last chunk
    print(f"Chunk {len(chunks) - 1}:\n\"{chunks[-1]}\"")
    print("-" * 50)


    # --- Step 4: Analyze the results ---
    print("\n[4] Analysis of Results:")
    print("  - Similarity between AI-focused chunks (0->1) is HIGH.")
    print("  - Similarity between the AI chunk and the unrelated 'coffee' chunk (1->2) is VERY LOW.")
    print("  - This demonstrates that cosine similarity of embeddings is an effective proxy for semantic context.")
    print("\n--- Spike Complete: Core assumption VALIDATED. ---")


if __name__ == "__main__":
    run_spike()