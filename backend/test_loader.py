from app.loaders import load_legal_documents


documents = load_legal_documents()

print(f"Total LangChain Documents: {len(documents)}")

for document in documents[:5]:
    print("\n" + "=" * 80)
    print("SOURCE:", document.metadata.get("source_file"))
    print("PAGE:", document.metadata.get("page"))
    print("CONTENT:")
    print(document.page_content[:500])