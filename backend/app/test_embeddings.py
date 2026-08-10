"""
Manual test for the embedding pipeline.

Run from the project root:
    python -m backend.app.test_embeddings
"""

from backend.app.embeddings import (
    EMBEDDING_MODEL_NAME,
    get_embeddings,
)


def main():
    print("Loading embedding model...")
    print(f"Model: {EMBEDDING_MODEL_NAME}")

    embeddings = get_embeddings()

    print("Embedding model loaded successfully.\n")

    test_text = (
        "Every person shall be entitled to be dealt with in accordance "
        "with law and in accordance with the law."
    )

    print("Generating test embedding...")
    vector = embeddings.embed_query(test_text)

    print(f"Embedding generated successfully.")
    print(f"Vector dimensions: {len(vector)}")
    print(f"First 10 values: {vector[:10]}")


if __name__ == "__main__":
    main()