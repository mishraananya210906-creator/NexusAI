
from pathlib import Path
import joblib


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Load trained models
category_model = joblib.load(
    BASE_DIR / "models" / "category_classifier.pkl"
)

priority_model = joblib.load(
    BASE_DIR / "models" / "priority_classifier.pkl"
)


# Department mapping
DEPARTMENT_MAP = {
    "Account": "Account Support",
    "Billing": "Billing Support",
    "Bug": "Technical Support",
    "Subscription": "Subscription Support",
    "API": "Developer Support"
}


def predict_ticket(ticket_text):
    """Predict category, priority and department for a support ticket."""

    category = category_model.predict([ticket_text])[0]
    priority = priority_model.predict([ticket_text])[0]

    return {
        "ticket": ticket_text,
        "category": category,
        "priority": priority,
        "department": DEPARTMENT_MAP.get(
            category, "General Support"
        )
    }


if __name__ == "__main__":

    test_tickets = [
        "I paid for my subscription, but the payment was deducted twice.",
        "I forgot my password and cannot log into my account.",
        "The application crashes whenever I open the dashboard.",
        "How can I generate an API key?",
        "I want to upgrade my current subscription plan.",
        "My API endpoint is returning a server error."
    ]

    print("\n" + "=" * 55)
    print("       NEXUSAI MULTIPLE TICKET PREDICTIONS")
    print("=" * 55)

    for index, ticket in enumerate(test_tickets, start=1):

        result = predict_ticket(ticket)

        print(f"\nTICKET {index}")
        print("-" * 55)
        print(f"Text       : {result['ticket']}")
        print(f"Category   : {result['category']}")
        print(f"Priority   : {result['priority']}")
        print(f"Department : {result['department']}")

    print("\n" + "=" * 55)
    print("          PREDICTION TEST COMPLETED")
    print("=" * 55)
