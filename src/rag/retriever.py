
import faiss
import numpy as np

from fastembed import TextEmbedding
from text_chunker import split_text
from document_loader import load_documents


def search_documents(query, chunks, index, model, top_k=3):

    # Convert user question into an embedding
    query_embedding = list(model.query_embed(query))[0]

    query_vector = np.array(
        [list(query_embedding)],
        dtype="float32"
    )

    # Search FAISS for similar document chunks
    distances, indices = index.search(query_vector, min(top_k, len(chunks)))

    results = []

    for distance, idx in zip(distances[0], indices[0]):
        if idx != -1:
            results.append({
                "text": chunks[idx],
                "distance": float(distance)
            })

    return results


if __name__ == "__main__":

    documents = load_documents("docs")

    all_chunks = []

    for document in documents:
        all_chunks.extend(split_text(document["text"]))

    model = TextEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    embeddings = list(model.embed(all_chunks))

    vectors = np.array(
        [list(embedding) for embedding in embeddings],
        dtype="float32"
    )

    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)

    question = "How can I reset my password?"

    results = search_documents(
        question,
        all_chunks,
        index,
        model
    )

    print("NEXUSAI SEMANTIC SEARCH")
    print("-" * 35)
    print("Question:", question)

    for result in results:
        print("\nRetrieved information:")
        print(result["text"])
        print("Distance:", round(result["distance"], 4))
