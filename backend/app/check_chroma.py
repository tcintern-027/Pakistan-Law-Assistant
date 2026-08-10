from backend.app.vector_store import get_vector_store


def main():
    vector_store = get_vector_store()

    queries = [
        "10A",
        "fair trial",
        "fair trial and due process",
        "civil rights and obligations",
    ]

    for query in queries:
        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        results = vector_store.similarity_search(
            query,
            k=10,
        )

        for index, document in enumerate(results, start=1):
            print("-" * 80)
            print(f"Rank: {index}")
            print(f"Source: {document.metadata.get('source_file')}")
            print(f"Page: {document.metadata.get('page')}")
            print(f"Chunk: {document.metadata.get('chunk_id')}")
            print(document.page_content[:300])


if __name__ == "__main__":
    main()