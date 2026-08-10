from backend.app.services.rag_service import ask_question


question = "What does Article 10A of the Constitution of Pakistan provide?"

result = ask_question(question)

print("\n" + "=" * 80)
print("QUESTION")
print("=" * 80)
print(result["question"])

print("\n" + "=" * 80)
print("ANSWER")
print("=" * 80)
print(result["answer"])

print("\n" + "=" * 80)
print("SOURCES")
print("=" * 80)

for source in result["sources"]:
    print(source)