from backend.app.loaders import load_legal_documents
from backend.app.splitter import split_documents


def main():
    documents = load_legal_documents()
    chunks = split_documents(documents)

    for chunk in chunks:
        if (
            chunk.metadata.get("source_file") == "Constitution of Pakistan.pdf"
            and chunk.metadata.get("page") == 25
        ):
            print("=" * 80)
            print(f"Chunk ID: {chunk.metadata.get('chunk_id')}")
            print(f"Chunk Index: {chunk.metadata.get('chunk_index')}")
            print(f"Length: {len(chunk.page_content)}")
            print()
            print(chunk.page_content)
            print()


if __name__ == "__main__":
    main()