import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langsmith import Client
from langchain_groq import ChatGroq


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / "backend" / ".env"
RESULTS_FILE = BASE_DIR / "evaluation" / "results.json"


# --------------------------------------------------
# Environment
# --------------------------------------------------

load_dotenv(ENV_FILE, override=True)

LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "pakistan-law-assistant",
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant",
)

if not LANGSMITH_API_KEY:
    raise RuntimeError("LANGSMITH_API_KEY is missing.")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is missing.")


# --------------------------------------------------
# LangSmith client
# --------------------------------------------------

client = Client(
    api_key=LANGSMITH_API_KEY,
)


# --------------------------------------------------
# Judge model
# --------------------------------------------------

judge = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0,
)


# --------------------------------------------------
# Load evaluation results
# --------------------------------------------------

with open(RESULTS_FILE, "r", encoding="utf-8") as file:
    results = json.load(file)


# --------------------------------------------------
# Evaluation prompt
# --------------------------------------------------

JUDGE_PROMPT = """
You are an expert evaluator of a Pakistan law RAG assistant.

Evaluate the assistant response using the information provided below.

QUESTION:
{question}

EXPECTED ANSWER:
{expected_answer}

KEY FACTS:
{key_facts}

ASSISTANT ANSWER:
{answer}

RETRIEVED SOURCES:
{sources}

Evaluate three dimensions from 0 to 1.

1. CORRECTNESS
Does the answer correctly answer the question and agree with the expected answer?

2. RELEVANCE
Is the answer directly relevant to the question without unnecessary or unrelated information?

3. GROUNDEDNESS
Is the answer supported by the retrieved legal sources?
The assistant must not invent legal facts that are unsupported by the retrieved material.

IMPORTANT:
For no-answer or fictional-law questions, a response that correctly states
that the information is unavailable and does not fabricate an answer should
receive a high correctness and groundedness score.

Return ONLY valid JSON in exactly this format:

{{
  "correctness": 0.0,
  "relevance": 0.0,
  "groundedness": 0.0,
  "reason": "brief explanation"
}}
"""


def evaluate_result(item: dict) -> dict:
    prompt = JUDGE_PROMPT.format(
        question=item["question"],
        expected_answer=item["expected_answer"],
        key_facts=", ".join(item["key_facts"]),
        answer=item["answer"],
        sources=json.dumps(item["sources"], ensure_ascii=False),
    )

    response = judge.invoke(prompt)

    content = response.content.strip()

    # Remove accidental markdown code fences.
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    evaluation = json.loads(content)

    return evaluation


# --------------------------------------------------
# Run evaluation
# --------------------------------------------------

print(f"Evaluating {len(results)} results...\n")

evaluated_results = []

for index, item in enumerate(results, start=1):

    print(
        f"[{index}/{len(results)}] "
        f"{item['id']} - {item['question']}"
    )

    evaluation = evaluate_result(item)

    evaluated_results.append(
        {
            "id": item["id"],
            "question": item["question"],
            "category": item["category"],
            "correctness": evaluation["correctness"],
            "relevance": evaluation["relevance"],
            "groundedness": evaluation["groundedness"],
            "reason": evaluation["reason"],
        }
    )


# --------------------------------------------------
# Calculate averages
# --------------------------------------------------

count = len(evaluated_results)

avg_correctness = (
    sum(x["correctness"] for x in evaluated_results) / count
)

avg_relevance = (
    sum(x["relevance"] for x in evaluated_results) / count
)

avg_groundedness = (
    sum(x["groundedness"] for x in evaluated_results) / count
)


summary = {
    "test_cases": count,
    "correctness": round(avg_correctness, 4),
    "relevance": round(avg_relevance, 4),
    "groundedness": round(avg_groundedness, 4),
}


# --------------------------------------------------
# Save evaluation report
# --------------------------------------------------

output = {
    "summary": summary,
    "results": evaluated_results,
}

OUTPUT_FILE = BASE_DIR / "evaluation" / "evaluation_report.json"

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8",
) as file:
    json.dump(
        output,
        file,
        indent=2,
        ensure_ascii=False,
    )


# --------------------------------------------------
# Print summary
# --------------------------------------------------

print("\n" + "=" * 60)
print("EVALUATION COMPLETE")
print("=" * 60)

print(f"Test cases:   {count}")
print(f"Correctness:  {avg_correctness:.2%}")
print(f"Relevance:    {avg_relevance:.2%}")
print(f"Groundedness: {avg_groundedness:.2%}")

print("\nReport saved to:")
print(OUTPUT_FILE)