"""
Manual test for the legal retrieval layer.

Run from the project root:
    python -m backend.app.test_retriever
"""

from backend.app.retriever import retrieve_documents


TEST_QUERIES = [
    "What is the right to fair trial?",
    "What does Article 10A say?",
    "What fundamental right protects fair trial and due process?",
    "What is the punishment for murder?",
    "What is freedom of speech in Pakistan?",
]


def main():
    for query in TEST_QUERIES:
        print("\n" + "=" * 80)
        print(f"QUERY: {query}")
        print("=" * 80)

        results = retrieve_documents(query, k=3)

        for index, document in enumerate(results, start=1):
            print("-" * 80)
            print(f"Rank: {index}")
            print(f"Source: {document.metadata.get('source_file')}")
            print(f"Page: {document.metadata.get('page')}")
            print(f"Chunk ID: {document.metadata.get('chunk_id')}")
            print()
            print(document.page_content[:600])


if __name__ == "__main__":
    main()