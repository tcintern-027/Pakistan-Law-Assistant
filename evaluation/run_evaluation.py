"""
Run the Pakistan Law Assistant against the evaluation dataset.

This script:
1. Loads the 15 evaluation cases.
2. Runs each question through the existing RAG service.
3. Stores the generated answer and retrieved sources.
4. Saves the results for later evaluation.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import json

from backend.app.services.rag_service import ask_question


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "evaluation" / "dataset.json"
RESULTS_PATH = BASE_DIR / "evaluation" / "results.json"


def load_dataset() -> list[dict]:
    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def run_evaluation(dataset: list[dict]) -> list[dict]:
    results = []

    for index, test_case in enumerate(dataset, start=1):
        question = test_case["question"]

        print(f"[{index}/{len(dataset)}] {question}")

        try:
            response = ask_question(question)

            result = {
                "id": test_case["id"],
                "question": question,
                "expected_answer": test_case["expected_answer"],
                "key_facts": test_case["key_facts"],
                "category": test_case["category"],
                "answer": response["answer"],
                "sources": response["sources"],
                "error": None,
            }

        except Exception as exc:
            result = {
                "id": test_case["id"],
                "question": question,
                "expected_answer": test_case["expected_answer"],
                "key_facts": test_case["key_facts"],
                "category": test_case["category"],
                "answer": None,
                "sources": [],
                "error": str(exc),
            }

        results.append(result)

    return results


def save_results(results: list[dict]) -> None:
    with open(RESULTS_PATH, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)


def main() -> None:
    dataset = load_dataset()

    print(f"Loaded {len(dataset)} evaluation cases.")
    print()

    results = run_evaluation(dataset)

    save_results(results)

    successful = sum(1 for result in results if result["error"] is None)
    failed = len(results) - successful

    print()
    print("Evaluation run complete.")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Results saved to: {RESULTS_PATH}")


if __name__ == "__main__":
    main()