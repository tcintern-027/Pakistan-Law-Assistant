from backend.app.loaders import load_legal_documents
from backend.app.splitter import split_documents
from backend.app.vector_store import add_documents, get_collection_count


def main():
    print("Loading legal documents...")
    documents = load_legal_documents()
    print(f"Loaded pages: {len(documents)}")

    print("Splitting documents...")
    chunks = split_documents(documents)
    print(f"Created chunks: {len(chunks)}")

    print("Adding chunks to ChromaDB...")
    add_documents(chunks)

    print(f"ChromaDB documents: {get_collection_count()}")
    print("Indexing complete.")


if __name__ == "__main__":
    main()