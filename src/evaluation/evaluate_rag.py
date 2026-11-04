
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from fastembed import TextEmbedding
from src.rag.document_loader import load_documents
from src.rag.text_chunker import create_document_chunks
from src.rag.hybrid_retriever import hybrid_search


def evaluate_recall():
    dataset_path = (
        PROJECT_ROOT / "data" / "evaluation" / "rag_questions.json"
    )

    with open(dataset_path, "r", encoding="utf-8") as file:
        questions = json.load(file)

    documents = load_documents(PROJECT_ROOT / "docs")
    chunks = create_document_chunks(documents)

    model = TextEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    hits_at_1 = 0
    hits_at_3 = 0
    hits_at_5 = 0
    reciprocal_ranks = []

    results = []

    for item in questions:
        retrieved = hybrid_search(
            query=item["question"],
            chunks=chunks,
            model=model,
            user_role="user",
            top_k=5
        )

        retrieved_sources = [
            result["filename"] for result in retrieved
        ]

        expected_source = item["expected_source"]

        rank = None

        for index, source in enumerate(retrieved_sources, start=1):
            if source == expected_source:
                rank = index
                break

        if rank is not None:
            reciprocal_ranks.append(1 / rank)

            if rank <= 1:
                hits_at_1 += 1

            if rank <= 3:
                hits_at_3 += 1

            if rank <= 5:
                hits_at_5 += 1
        else:
            reciprocal_ranks.append(0)

        results.append({
            "question": item["question"],
            "expected_source": expected_source,
            "retrieved_sources": retrieved_sources,
            "correct_document_rank": rank
        })

    total = len(questions)

    recall_at_1 = hits_at_1 / total if total else 0
    recall_at_3 = hits_at_3 / total if total else 0
    recall_at_5 = hits_at_5 / total if total else 0

    mrr = (
        sum(reciprocal_ranks) / total if total else 0
    )

    report = {
        "total_questions": total,
        "recall_at_1": round(recall_at_1, 4),
        "recall_at_3": round(recall_at_3, 4),
        "recall_at_5": round(recall_at_5, 4),
        "mean_reciprocal_rank": round(mrr, 4),
        "results": results
    }

    output_path = (
        PROJECT_ROOT / "data" / "evaluation" / "rag_report.json"
    )

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\n===== NEXUSAI RAG EVALUATION =====")
    print(f"Total questions: {total}")
    print(f"Recall@1: {recall_at_1:.2%}")
    print(f"Recall@3: {recall_at_3:.2%}")
    print(f"Recall@5: {recall_at_5:.2%}")
    print(f"MRR: {mrr:.4f}")
    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    evaluate_recall()
