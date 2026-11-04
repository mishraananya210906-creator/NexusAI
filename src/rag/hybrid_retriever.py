
import numpy as np
import faiss

from fastembed import TextEmbedding
from rank_bm25 import BM25Okapi

from src.rag.document_loader import load_documents
from src.rag.text_chunker import create_document_chunks


def hybrid_search(query, chunks, model, user_role, top_k=3):

    # 1. Filter documents BEFORE retrieval
    accessible_chunks = [
        chunk for chunk in chunks
        if user_role in chunk.get("allowed_roles", [])
    ]

    if not accessible_chunks:
        return []

    texts = [chunk["text"] for chunk in accessible_chunks]

    # 2. Generate document embeddings
    embeddings = list(model.embed(texts))

    vectors = np.array(
        [list(embedding) for embedding in embeddings],
        dtype="float32"
    )

    # 3. Semantic search using FAISS
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    query_embedding = list(model.query_embed(query))[0]

    query_vector = np.array(
        [list(query_embedding)],
        dtype="float32"
    )

    search_k = min(top_k, len(accessible_chunks))

    distances, semantic_indices = index.search(
        query_vector,
        len(accessible_chunks)
    )

    # 4. Keyword search using BM25
    tokenized_chunks = [
        text.lower().split() for text in texts
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    keyword_scores = bm25.get_scores(query.lower().split())

    keyword_indices = np.argsort(keyword_scores)[::-1]

    # 5. Combine rankings using Reciprocal Rank Fusion
    combined_scores = {}

    for rank, idx in enumerate(semantic_indices[0]):
        idx = int(idx)

        combined_scores[idx] = combined_scores.get(idx, 0) + (
            1 / (60 + rank + 1)
        )

    for rank, idx in enumerate(keyword_indices):
        idx = int(idx)

        combined_scores[idx] = combined_scores.get(idx, 0) + (
            1 / (60 + rank + 1)
        )

    ranked_results = sorted(
        combined_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    # 6. Return authorized results with source references
    results = []

    for idx, score in ranked_results[:search_k]:

        chunk = accessible_chunks[idx]

        results.append({
            "text": chunk["text"],
            "filename": chunk["filename"],
            "source": chunk["source"],
            "chunk_number": chunk["chunk_number"],
            "page": chunk.get("page"),
            "score": round(float(score), 5)
        })

    return results


# ----------------------------------------
# TEST HYBRID RETRIEVAL
# ----------------------------------------

if __name__ == "__main__":

    documents = load_documents("docs")
    chunks = create_document_chunks(documents)

    model = TextEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    question = "How can I reset my password?"
    user_role = "user"

    results = hybrid_search(
        question,
        chunks,
        model,
        user_role
    )

    print("NEXUSAI SECURE HYBRID RETRIEVAL")
    print("-" * 45)

    print("User role:", user_role)
    print("Question:", question)

    for result in results:

        print("\nRetrieved information:")
        print(result["text"])

        print("Source:", result["source"])
        print("Filename:", result["filename"])
        print("Chunk:", result["chunk_number"])
        print("Score:", result["score"])

    print("\nSecure retrieval completed!")
