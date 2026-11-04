
# NexusAI Document-Level Access Control

VALID_ROLES = {"user", "support_agent", "admin"}


def filter_documents_by_role(chunks, user_role):

    # Reject unknown roles
    if user_role not in VALID_ROLES:
        return []

    accessible_chunks = []

    for chunk in chunks:

        allowed_roles = chunk.get("allowed_roles", [])

        if not isinstance(allowed_roles, list):
            continue

        if user_role in allowed_roles:
            accessible_chunks.append(chunk)

    return accessible_chunks


if __name__ == "__main__":

    sample_chunks = [
        {
            "text": "Public account guide",
            "allowed_roles": ["user", "support_agent", "admin"]
        },
        {
            "text": "Internal support procedure",
            "allowed_roles": ["support_agent", "admin"]
        },
        {
            "text": "Administrator security policy",
            "allowed_roles": ["admin"]
        }
    ]

    for role in ["user", "support_agent", "admin", "guest"]:

        results = filter_documents_by_role(sample_chunks, role)

        print("\nCurrent role:", role)
        print("Accessible documents:", len(results))

        for document in results:
            print("-", document["text"])
