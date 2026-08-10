from backend.app.loaders import load_legal_documents


def main():
    documents = load_legal_documents()

    terms = [
        "fair trial",
        "FAIR TRIAL",
        "Article 10A",
        "ARTICLE 10A",
        "10-A",
    ]

    for term in terms:
        print("\n" + "=" * 80)
        print(f"SEARCH TERM: {term}")
        print("=" * 80)

        found = 0

        for document in documents:
            if term.lower() in document.page_content.lower():
                print("-" * 80)
                print(f"Source: {document.metadata.get('source_file')}")
                print(f"Page: {document.metadata.get('page')}")

                text = document.page_content
                position = text.lower().find(term.lower())

                start = max(0, position - 500)
                end = min(len(text), position + 1500)

                print(text[start:end])

                found += 1

                if found >= 10:
                    break

        print(f"\nMatches found: {found}")


if __name__ == "__main__":
    main()