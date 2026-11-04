
import re


def split_text(text, chunk_size=500, overlap=100):

    # Split text using headings and blank lines
    sections = re.split(r"\n\s*\n", text.strip())

    chunks = []
    current_chunk = ""

    for section in sections:

        section = section.strip()

        if not section:
            continue

        # Keep sections together whenever possible
        if len(section) <= chunk_size:

            if not current_chunk:
                current_chunk = section

            elif len(current_chunk) + len(section) + 2 <= chunk_size:
                current_chunk += "\n\n" + section

            else:
                chunks.append(current_chunk)
                current_chunk = section

        else:

            # Save the current chunk before splitting a large section
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            # Split very large sections into smaller overlapping chunks
            start = 0

            while start < len(section):

                end = start + chunk_size
                part = section[start:end].strip()

                if part:
                    chunks.append(part)

                start += chunk_size - overlap

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def create_document_chunks(documents):

    all_chunks = []

    for document in documents:

        text_chunks = split_text(document["text"])

        for chunk_number, chunk in enumerate(text_chunks, start=1):

            chunk_data = {
                "text": chunk,
                "filename": document["filename"],
                "source": document["source"],
                "file_type": document["file_type"],
                "allowed_roles": document["allowed_roles"],
                "chunk_number": chunk_number
            }

            if "page" in document:
                chunk_data["page"] = document["page"]

            all_chunks.append(chunk_data)

    return all_chunks


if __name__ == "__main__":

    from src.rag.document_loader import load_documents

    documents = load_documents("docs")

    chunks = create_document_chunks(documents)

    print("NEXUSAI SECURE DOCUMENT CHUNKER")
    print("-" * 40)

    print("Total chunks:", len(chunks))

    for chunk in chunks:

        print("\nFilename:", chunk["filename"])
        print("Chunk:", chunk["chunk_number"])
        print("Allowed roles:", chunk["allowed_roles"])
        print("Source:", chunk["source"])
        print("Text:", chunk["text"])

    print("\nSecure chunking completed!")
