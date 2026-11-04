
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from src.rag.access_control import filter_documents_by_role


def test_user_access():

    chunks = [
        {
            "text": "Public guide",
            "allowed_roles": ["user", "support_agent", "admin"]
        },
        {
            "text": "Internal guide",
            "allowed_roles": ["support_agent", "admin"]
        },
        {
            "text": "Admin policy",
            "allowed_roles": ["admin"]
        }
    ]

    user_results = filter_documents_by_role(chunks, "user")
    assert len(user_results) == 1

    support_results = filter_documents_by_role(
        chunks, "support_agent"
    )
    assert len(support_results) == 2

    admin_results = filter_documents_by_role(chunks, "admin")
    assert len(admin_results) == 3

    unknown_results = filter_documents_by_role(
        chunks, "unknown"
    )
    assert len(unknown_results) == 0

    print("User access test: PASSED")
    print("Support agent access test: PASSED")
    print("Admin access test: PASSED")
    print("Unknown role access test: PASSED")


if __name__ == "__main__":
    test_user_access()
    print("\nAll access-control tests passed!")
