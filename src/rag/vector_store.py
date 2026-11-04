
import faiss
import numpy as np

from embedding_generator import generate_embeddings
from text_chunker import split_text
from document_loader import load_documents


def create_vector_store(chunks):
    embeddings = generate_embeddings(chunks)

    # Convert embeddings into a NumPy array
    vectors = np.array(
        [list(embedding) for embedding in embeddings],
        dtype="float32"
    )

    # Create FAISS index
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Store vectors
    index.add(vectors)

    return index


if __name__ == "__main__":
    documents = load_documents("docs")

    all_chunks = []

    for document in documents:
        chunks = split_text(document["text"])
        all_chunks.extend(chunks)

    index = create_vector_store(all_chunks)

    print("NEXUSAI VECTOR DATABASE")
    print("-" * 35)
    print("Vectors stored:", index.ntotal)
    print("Vector dimensions:", index.d)
    print("FAISS index created successfully!")
