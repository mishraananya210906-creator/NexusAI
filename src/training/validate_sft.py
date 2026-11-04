
import json
from pathlib import Path

# Locate the SFT dataset
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "processed" / "training" / "sft_train.jsonl"


def validate_sft_dataset():

    valid_examples = 0
    errors = []

    with open(DATA_FILE, "r", encoding="utf-8") as file:

        for line_number, line in enumerate(file, start=1):

            try:
                example = json.loads(line)

                messages = example.get("messages", [])

                if len(messages) != 2:
                    errors.append(
                        f"Line {line_number}: Expected 2 messages."
                    )
                    continue

                if messages[0].get("role") != "user":
                    errors.append(
                        f"Line {line_number}: First message must be user."
                    )
                    continue

                if messages[1].get("role") != "assistant":
                    errors.append(
                        f"Line {line_number}: Second message must be assistant."
                    )
                    continue

                if not messages[0].get("content", "").strip():
                    errors.append(
                        f"Line {line_number}: User message is empty."
                    )
                    continue

                if not messages[1].get("content", "").strip():
                    errors.append(
                        f"Line {line_number}: Assistant message is empty."
                    )
                    continue

                valid_examples += 1

            except json.JSONDecodeError:
                errors.append(
                    f"Line {line_number}: Invalid JSON."
                )

    print("\n===== NEXUSAI SFT DATASET VALIDATION =====")
    print(f"Valid examples: {valid_examples}")
    print(f"Errors found: {len(errors)}")

    if errors:
        for error in errors:
            print(error)
    else:
        print("SFT dataset validation successful!")


if __name__ == "__main__":
    validate_sft_dataset()

