
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "support_tickets.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "evaluation" / "priority_review.csv"


def suggest_priority(text):

    text = text.lower()

    high_keywords = [
        "cannot log in",
        "cannot access my account",
        "account has been temporarily locked",
        "unknown login",
        "without permission",
        "changed my account information",
        "charged twice",
        "charged after cancellation",
        "money was deducted",
        "service i did not purchase",
        "crashes",
        "blank screen",
        "server error",
        "stopped working",
        "key has stopped working",
        "unauthorized error",
        "completely unavailable"
    ]

    medium_keywords = [
        "not working",
        "incorrect",
        "not arrived",
        "pending",
        "not updating",
        "not responding",
        "slowly",
        "too long",
        "missing fields",
        "invalid json",
        "unexpected status",
        "not reflected",
        "not loading",
        "not reaching",
        "not showing",
        "not available",
        "timing out",
        "rate limit"
    ]

    if any(keyword in text for keyword in high_keywords):
        return "High"

    if any(keyword in text for keyword in medium_keywords):
        return "Medium"

    return "Low"


def main():

    df = pd.read_csv(DATA_PATH)

    df["suggested_priority"] = df["text"].apply(suggest_priority)

    df["needs_review"] = (
        df["priority"] != df["suggested_priority"]
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print("=" * 45)
    print("NEXUSAI PRIORITY REVIEW")
    print("=" * 45)

    print("Total tickets:", len(df))

    print(
        "Tickets matching suggested priority:",
        (df["needs_review"] == False).sum()
    )

    print(
        "Tickets needing manual review:",
        df["needs_review"].sum()
    )

    print("\nSuggested priority distribution:")

    print(df["suggested_priority"].value_counts())

    print("\nReview report saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
