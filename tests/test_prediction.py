
from src.triage.predict_ticket import predict_ticket


def test_billing_ticket_prediction():
    result = predict_ticket(
        "My payment was deducted twice."
    )

    assert result["category"] == "Billing"
    assert result["priority"] == "High"
    assert result["department"] == "Billing Support"


def test_account_ticket_prediction():
    result = predict_ticket(
        "I forgot my password and cannot log in."
    )

    assert result["category"] == "Account"
    assert result["priority"] == "High"
    assert result["department"] == "Account Support"


def test_bug_ticket_prediction():
    result = predict_ticket(
        "The application crashes when I open it."
    )

    assert result["category"] == "Bug"
    assert result["priority"] == "High"
    assert result["department"] == "Technical Support"


def test_api_ticket_prediction():
    result = predict_ticket(
        "How can I generate an API key?"
    )

    assert result["category"] == "API"
    assert result["priority"] == "Low"
    assert result["department"] == "Developer Support"


def test_subscription_ticket_prediction():
    result = predict_ticket(
        "I want to upgrade my subscription plan."
    )

    assert result["category"] == "Subscription"
    assert result["priority"] == "Low"
    assert result["department"] == "Subscription Support"


def test_prediction_response_structure():
    result = predict_ticket(
        "My application is not working."
    )

    assert set(result.keys()) == {
        "ticket",
        "category",
        "priority",
        "department"
    }


def test_prediction_returns_valid_priority():
    result = predict_ticket(
        "My payment is not working."
    )

    assert result["priority"] in [
        "High",
        "Medium",
        "Low"
    ]


def test_prediction_returns_valid_category():
    result = predict_ticket(
        "I need help with my account."
    )

    assert result["category"] in [
        "Account",
        "Billing",
        "Bug",
        "Subscription",
        "API"
    ]
