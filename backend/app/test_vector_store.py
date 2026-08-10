"""
Diagnostic retrieval test for the Pakistan Law Assistant.

Tests whether the vector store retrieves the correct legal provisions
for several Article 10A queries.
"""

from backend.app.vector_store import get_vector_store


QUERIES = [
    "Article 10A",
    "right to fair trial",
    "fair trial and due process",
    "civil rights and obligations",
]


def main():
    vector_store = get_vector_store()

    for query in QUERIES:
        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        results = vector_store.similarity_search_with_score(
            query,
            k=5,
        )

        for index, (document, score) in enumerate(results, start=1):
            print("-" * 80)
            print(f"Rank: {index}")
            print(f"Score: {score:.6f}")
            print(f"Source: {document.metadata.get('source_file')}")
            print(f"Page: {document.metadata.get('page')}")
            print(f"Chunk ID: {document.metadata.get('chunk_id')}")
            print("Content:")
            print(document.page_content[:700])


if __name__ == "__main__":
    main()