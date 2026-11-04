import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "support_tickets.csv"

new_tickets = [
    # ACCOUNT: 15 additional tickets
    ("Account login fails after entering the correct password.", "Account", "High", "Account Support"),
    ("I need to change my registered phone number.", "Account", "Medium", "Account Support"),
    ("My account has been temporarily locked.", "Account", "High", "Account Support"),
    ("I am unable to verify my email address.", "Account", "Medium", "Account Support"),
    ("I forgot my account password and cannot sign in.", "Account", "High", "Account Support"),
    ("My profile information is not updating.", "Account", "Low", "Account Support"),
    ("I received an alert about an unknown login.", "Account", "High", "Account Support"),
    ("How can I delete my existing account?", "Account", "Medium", "Account Support"),
    ("My account verification link has expired.", "Account", "Medium", "Account Support"),
    ("I cannot access my account settings.", "Account", "Medium", "Account Support"),
    ("My username is not being recognized.", "Account", "High", "Account Support"),
    ("I want to update my personal details.", "Account", "Low", "Account Support"),
    ("The password reset email never arrived.", "Account", "Medium", "Account Support"),
    ("Someone changed my account information without permission.", "Account", "High", "Account Support"),
    ("My account registration is still pending.", "Account", "Low", "Account Support"),

    # BILLING: 15 additional tickets
    ("My credit card was charged twice for one order.", "Billing", "High", "Billing Support"),
    ("The payment failed but money was deducted.", "Billing", "High", "Billing Support"),
    ("I need an invoice for my recent payment.", "Billing", "Low", "Billing Support"),
    ("My refund has not arrived yet.", "Billing", "Medium", "Billing Support"),
    ("The amount charged is different from the displayed price.", "Billing", "High", "Billing Support"),
    ("Where can I download my billing statement?", "Billing", "Low", "Billing Support"),
    ("My payment transaction is still pending.", "Billing", "Medium", "Billing Support"),
    ("I was charged for a service I did not purchase.", "Billing", "High", "Billing Support"),
    ("My invoice contains incorrect billing details.", "Billing", "Medium", "Billing Support"),
    ("The payment gateway shows an error.", "Billing", "Medium", "Billing Support"),
    ("I want to know the status of my refund.", "Billing", "Low", "Billing Support"),
    ("My bank transfer is not reflected in my account.", "Billing", "Medium", "Billing Support"),
    ("The billing page displays an incorrect amount.", "Billing", "High", "Billing Support"),
    ("I need clarification about a transaction on my statement.", "Billing", "Low", "Billing Support"),
    ("My subscription payment was processed unexpectedly.", "Billing", "High", "Billing Support"),

    # BUG: 16 additional tickets
    ("The application crashes when I click the submit button.", "Bug", "High", "Technical Support"),
    ("The dashboard is displaying a blank screen.", "Bug", "High", "Technical Support"),
    ("The search function returns incorrect results.", "Bug", "Medium", "Technical Support"),
    ("Images are not loading on the homepage.", "Bug", "Medium", "Technical Support"),
    ("The application freezes after opening the settings page.", "Bug", "High", "Technical Support"),
    ("I receive an error whenever I upload a file.", "Bug", "Medium", "Technical Support"),
    ("The notification button does not respond.", "Bug", "Low", "Technical Support"),
    ("The website layout breaks on mobile devices.", "Bug", "Medium", "Technical Support"),
    ("The save button does not store my changes.", "Bug", "High", "Technical Support"),
    ("The application takes too long to load.", "Bug", "Medium", "Technical Support"),
    ("The filter option is not working correctly.", "Bug", "Low", "Technical Support"),
    ("I cannot download reports from the dashboard.", "Bug", "Medium", "Technical Support"),
    ("The page displays an unexpected error after refreshing.", "Bug", "High", "Technical Support"),
    ("The application does not display the latest updates.", "Bug", "Low", "Technical Support"),
    ("The navigation menu disappears when scrolling.", "Bug", "Low", "Technical Support"),
    ("The export feature produces an empty file.", "Bug", "Medium", "Technical Support"),

    # SUBSCRIPTION: 17 additional tickets
    ("I want to upgrade my current subscription plan.", "Subscription", "Low", "Subscription Support"),
    ("My subscription expired before its renewal date.", "Subscription", "High", "Subscription Support"),
    ("How can I cancel my subscription?", "Subscription", "Low", "Subscription Support"),
    ("My premium subscription benefits are unavailable.", "Subscription", "High", "Subscription Support"),
    ("I want to switch to a different subscription plan.", "Subscription", "Medium", "Subscription Support"),
    ("My subscription renewal failed.", "Subscription", "High", "Subscription Support"),
    ("How do I check my subscription expiry date?", "Subscription", "Low", "Subscription Support"),
    ("My plan was downgraded without my request.", "Subscription", "High", "Subscription Support"),
    ("I cannot access features included in my plan.", "Subscription", "Medium", "Subscription Support"),
    ("I want to pause my subscription temporarily.", "Subscription", "Low", "Subscription Support"),
    ("My subscription is not showing in my profile.", "Subscription", "Medium", "Subscription Support"),
    ("The automatic renewal option is not working.", "Subscription", "Medium", "Subscription Support"),
    ("I need information about available subscription plans.", "Subscription", "Low", "Subscription Support"),
    ("My subscription was cancelled unexpectedly.", "Subscription", "High", "Subscription Support"),
    ("I want to reactivate my expired subscription.", "Subscription", "Medium", "Subscription Support"),
    ("The subscription page shows the wrong renewal date.", "Subscription", "Medium", "Subscription Support"),
    ("I cannot change my current subscription plan.", "Subscription", "Low", "Subscription Support"),

    # API: 17 additional tickets
    ("My API request returns an unauthorized error.", "API", "High", "Developer Support"),
    ("The API response contains missing fields.", "API", "Medium", "Developer Support"),
    ("I cannot generate a new API key.", "API", "High", "Developer Support"),
    ("The API endpoint is returning a server error.", "API", "High", "Developer Support"),
    ("How can I authenticate my API requests?", "API", "Low", "Developer Support"),
    ("The API rate limit is blocking my requests.", "API", "Medium", "Developer Support"),
    ("My API integration stopped working.", "API", "High", "Developer Support"),
    ("The API documentation does not explain this endpoint.", "API", "Low", "Developer Support"),
    ("I am receiving invalid JSON from the API.", "API", "Medium", "Developer Support"),
    ("The API connection is timing out.", "API", "High", "Developer Support"),
    ("How can I configure API authentication?", "API", "Low", "Developer Support"),
    ("The API returns an unexpected status code.", "API", "Medium", "Developer Support"),
    ("My API key has stopped working.", "API", "High", "Developer Support"),
    ("I need help integrating the API with my application.", "API", "Low", "Developer Support"),
    ("The API pagination feature is returning duplicate records.", "API", "Medium", "Developer Support"),
    ("The webhook notification is not reaching my server.", "API", "Medium", "Developer Support"),
    ("The API request payload is being rejected.", "API", "High", "Developer Support"),
]


def expand_dataset():
    with open(DATA_PATH, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        original_tickets = list(reader)
        fieldnames = reader.fieldnames

    if not fieldnames or not {"ticket_id", "text", "category", "priority", "department"}.issubset(fieldnames):
        raise ValueError("Unexpected CSV structure. Check the original dataset.")

    existing_ids = {row["ticket_id"] for row in original_tickets}

    if len(original_tickets) != 20:
        raise ValueError(
            f"Expected 20 original tickets, found {len(original_tickets)}. "
            "Check the dataset before expanding."
        )

    new_rows = []

    for index, (text, category, priority, department) in enumerate(new_tickets, start=21):
        ticket_id = f"T{index:03d}"

        if ticket_id in existing_ids:
            raise ValueError(f"Duplicate ticket ID: {ticket_id}")

        new_rows.append({
            "ticket_id": ticket_id,
            "text": text,
            "category": category,
            "priority": priority,
            "department": department
        })

    all_tickets = original_tickets + new_rows

    with open(DATA_PATH, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_tickets)

    print("===== NEXUSAI DATASET EXPANSION =====")
    print(f"Original tickets: {len(original_tickets)}")
    print(f"New tickets added: {len(new_rows)}")
    print(f"Total tickets: {len(all_tickets)}")

    print("\nCategory distribution:")
    for category in sorted({row["category"] for row in all_tickets}):
        count = sum(row["category"] == category for row in all_tickets)
        print(f"{category}: {count}")

    print("\nPriority distribution:")
    for priority in sorted({row["priority"] for row in all_tickets}):
        count = sum(row["priority"] == priority for row in all_tickets)
        print(f"{priority}: {count}")


if __name__ == "__main__":
    expand_dataset()