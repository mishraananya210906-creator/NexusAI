
from pathlib import Path
from pypdf import PdfReader


def get_allowed_roles(filename):

    filename = filename.lower()

    if filename.startswith("admin_"):
        return ["admin"]

    elif filename.startswith("internal_"):
        return ["support_agent", "admin"]

    else:
        return ["user", "support_agent", "admin"]


def load_documents(folder_path):

    documents = []
    folder = Path(folder_path)

    for file_path in folder.iterdir():

        allowed_roles = get_allowed_roles(file_path.name)

        if file_path.suffix.lower() == ".txt":

            text = file_path.read_text(encoding="utf-8")

            documents.append({
                "filename": file_path.name,
                "source": str(file_path),
                "file_type": "text",
                "allowed_roles": allowed_roles,
                "text": text
            })

        elif file_path.suffix.lower() == ".pdf":

            reader = PdfReader(str(file_path))

            for page_number, page in enumerate(reader.pages, start=1):

                text = page.extract_text() or ""

                if text.strip():
                    documents.append({
                        "filename": file_path.name,
                        "source": str(file_path),
                        "file_type": "pdf",
                        "allowed_roles": allowed_roles,
                        "page": page_number,
                        "text": text
                    })

    return documents


if __name__ == "__main__":

    docs = load_documents("docs")

    print("NEXUSAI DOCUMENT PERMISSIONS")
    print("-" * 40)

    for doc in docs:
        print("\nFilename:", doc["filename"])
        print("Allowed roles:", doc["allowed_roles"])

    print("\nDocument permissions loaded!")

