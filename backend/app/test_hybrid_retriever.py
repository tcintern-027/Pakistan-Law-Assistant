"""Manual test for hybrid legal retrieval.

Run with:

python -m backend.app.test_hybrid_retriever
"""

from backend.app.retriever import retrieve_documents


def run_test(query: str) -> None:
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retrieve_documents(
        query,
        k=5,
        semantic_k=20,
    )

    for rank, document in enumerate(results, start=1):
        print("\n" + "-" * 80)
        print(f"Rank: {rank}")
        print(f"Source: {document.metadata.get('source_file')}")
        print(f"Page: {document.metadata.get('page')}")
        print(f"Chunk ID: {document.metadata.get('chunk_id')}")
        print(f"Chunk Index: {document.metadata.get('chunk_index')}")
        print(f"Content length: {len(document.page_content)}")
        print("\n" + document.page_content[:700])


def main():
    test_queries = [
        "Article 10A",
        "fair trial and due process",
        "Section 302",
        "kidnapping",
    ]

    for query in test_queries:
        run_test(query)


if __name__ == "__main__":
    main()