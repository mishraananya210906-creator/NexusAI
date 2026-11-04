
from fastembed import TextEmbedding
from text_chunker import split_text
from document_loader import load_documents


def generate_embeddings(texts):
    model = TextEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    embeddings = list(model.embed(texts))

    return embeddings


if __name__ == "__main__":
    documents = load_documents("docs")

    all_chunks = []

    for document in documents:
        chunks = split_text(document["text"])
        all_chunks.extend(chunks)

    print("NEXUSAI EMBEDDING GENERATOR")
    print("-" * 35)

    print("Total chunks:", len(all_chunks))

    embeddings = generate_embeddings(all_chunks)

    print("Total embeddings:", len(embeddings))

    if embeddings:
        print("Embedding dimensions:", len(embeddings[0]))

    print("\nEmbedding generation completed!")
