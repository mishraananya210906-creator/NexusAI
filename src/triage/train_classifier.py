
import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    f1_score
)


# 1. PROJECT PATHS

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "support_tickets.csv"
MODEL_DIR = PROJECT_ROOT / "models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)


# 2. LOAD DATASET

print("=" * 50)
print("NEXUSAI SUPPORT TICKET CLASSIFIER")
print("=" * 50)

df = pd.read_csv(DATA_PATH)

df = df.dropna(subset=["text", "category", "priority"])

df["text"] = df["text"].astype(str)
df["category"] = df["category"].astype(str).str.strip()
df["priority"] = df["priority"].astype(str).str.strip()

X = df["text"]

y_category = df["category"]
y_priority = df["priority"]

print("Total usable tickets:", len(df))


# 3. CLASSIFIER PIPELINE

def create_classifier():

    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                stop_words="english",
                ngram_range=(1, 2)
            )
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            )
        )
    ])


# 4. EVALUATE CATEGORY CLASSIFIER

print("\n" + "=" * 50)
print("CATEGORY CLASSIFIER EVALUATION")
print("=" * 50)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_category,
    test_size=0.25,
    random_state=42,
    stratify=y_category
)

evaluation_category_model = create_classifier()

evaluation_category_model.fit(X_train, y_train)

predictions = evaluation_category_model.predict(X_test)

print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))
print("Accuracy:", round(accuracy_score(y_test, predictions), 4))

print(
    "Macro-F1:",
    round(f1_score(y_test, predictions, average="macro", zero_division=0), 4)
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# 5. EVALUATE PRIORITY CLASSIFIER

print("\n" + "=" * 50)
print("PRIORITY CLASSIFIER EVALUATION")
print("=" * 50)

X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X,
    y_priority,
    test_size=0.25,
    random_state=42,
    stratify=y_priority
)

evaluation_priority_model = create_classifier()

evaluation_priority_model.fit(X_train_p, y_train_p)

priority_predictions = evaluation_priority_model.predict(X_test_p)

print("Training examples:", len(X_train_p))
print("Testing examples:", len(X_test_p))
print("Accuracy:", round(accuracy_score(y_test_p, priority_predictions), 4))

print(
    "Macro-F1:",
    round(
        f1_score(
            y_test_p,
            priority_predictions,
            average="macro",
            zero_division=0
        ),
        4
    )
)

print("\nClassification Report:")

print(
    classification_report(
        y_test_p,
        priority_predictions,
        zero_division=0
    )
)


# 6. TRAIN FINAL CATEGORY MODEL ON ALL DATA

print("\n" + "=" * 50)
print("TRAINING FINAL MODELS ON ALL DATA")
print("=" * 50)

final_category_model = create_classifier()

final_category_model.fit(X, y_category)

joblib.dump(
    final_category_model,
    MODEL_DIR / "category_classifier.pkl"
)

print("Final category model saved!")


# 7. TRAIN FINAL PRIORITY MODEL ON ALL DATA

final_priority_model = create_classifier()

final_priority_model.fit(X, y_priority)

joblib.dump(
    final_priority_model,
    MODEL_DIR / "priority_classifier.pkl"
)

print("Final priority model saved!")


# 8. COMPLETION

print("\n" + "=" * 50)
print("NEXUSAI TRAINING COMPLETED")
print("=" * 50)

print("Total records used for final training:", len(df))
print("Category model: models/category_classifier.pkl")
print("Priority model: models/priority_classifier.pkl")

print("\nBoth models are ready for inference!")
