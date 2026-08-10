"""
Manual inspection script for the text splitting pipeline.

Run from the project root:
    python backend/app/test_splitter.py
"""

from backend.app.loaders import load_legal_documents
from backend.app.splitter import split_documents, get_chunk_stats

def main():
    print("Loading legal documents...")
    documents = load_legal_documents()

    print(f"Loaded {len(documents)} page-level documents.\n")

    print("Splitting documents into chunks...")
    chunks = split_documents(documents)

    print(f"Produced {len(chunks)} chunks.\n")

    stats = get_chunk_stats(chunks)

    print("Chunk statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\nSample chunks:")

    for chunk in chunks[:5]:
        print("-" * 70)
        print(f"Source: {chunk.metadata.get('source_file')}")
        print(f"Page: {chunk.metadata.get('page')}")
        print(f"Chunk ID: {chunk.metadata.get('chunk_id')}")
        print(f"Chunk Index: {chunk.metadata.get('chunk_index')}")
        print(f"Content length: {len(chunk.page_content)} characters")
        print("Content:")
        print(chunk.page_content[:500])
        print()


if __name__ == "__main__":
    main()