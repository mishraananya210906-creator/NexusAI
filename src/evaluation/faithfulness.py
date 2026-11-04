
import re


def calculate_faithfulness(answer, retrieved_context):
    """
    Simple baseline faithfulness evaluator.
    Measures meaningful word overlap between
    an answer and its retrieved context.
    """

    if not answer.strip() or not retrieved_context.strip():
        return 0.0

    stop_words = {
        "the", "a", "an", "is", "are", "was", "were",
        "to", "of", "in", "on", "and", "or", "for",
        "can", "be", "with", "their", "they", "users"
    }

    answer_words = set(
        re.findall(r"\b[a-zA-Z]+\b", answer.lower())
    )

    context_words = set(
        re.findall(r"\b[a-zA-Z]+\b", retrieved_context.lower())
    )

    meaningful_words = answer_words - stop_words

    if not meaningful_words:
        return 0.0

    supported_words = meaningful_words.intersection(context_words)

    score = len(supported_words) / len(meaningful_words)

    return round(score, 4)


if __name__ == "__main__":

    context = """
    Users can reset their password by selecting
    the Forgot Password option. A reset link
    will be sent to their registered email.
    """

    answer = """
    Users must contact the billing department
    and provide their bank account details
    to reset their password.
    """

    score = calculate_faithfulness(answer, context)

    print("===== FAITHFULNESS EVALUATION =====")
    print(f"Faithfulness Score: {score:.2%}")

    if score >= 0.70:
        print("Result: High word overlap")
    elif score >= 0.40:
        print("Result: Moderate word overlap")
    else:
        print("Result: Low word overlap")
