
import sys
from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score
)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "support_tickets.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "evaluation"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def evaluate_model(target_column, model_name):

    df = pd.read_csv(DATA_PATH)

    df = df.dropna(subset=["text", target_column])

    X = df["text"].astype(str)
    y = df[target_column].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train_vectorized, y_train)

    predictions = model.predict(X_test_vectorized)

    accuracy = accuracy_score(y_test, predictions)

    macro_f1 = f1_score(
        y_test,
        predictions,
        average="macro",
        zero_division=0
    )

    report = classification_report(
        y_test,
        predictions,
        zero_division=0
    )

    labels = sorted(y.unique())

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=labels
    )

    print(f"\n===== {model_name} EVALUATION =====")
    print(f"Training examples: {len(X_train)}")
    print(f"Testing examples: {len(X_test)}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro-F1: {macro_f1:.4f}")

    print("\nClassification Report:")
    print(report)

    print("Confusion Matrix:")
    print(matrix)

    result = {
        "model": model_name,
        "accuracy": round(accuracy, 4),
        "macro_f1": round(macro_f1, 4),
        "classification_report": classification_report(
            y_test,
            predictions,
            output_dict=True,
            zero_division=0
        ),
        "confusion_matrix": matrix.tolist(),
        "labels": labels
    }

    output_path = OUTPUT_DIR / f"{model_name.lower()}_evaluation.json"

    with open(output_path, "w", encoding="utf-8") as file:
        import json
        json.dump(result, file, indent=4)

    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":

    evaluate_model("category", "Category_Classifier")

    evaluate_model("priority", "Priority_Classifier")
