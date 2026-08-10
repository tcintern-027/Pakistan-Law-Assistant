from backend.app.llm import get_llm


llm = get_llm()

response = llm.invoke(
    "In one sentence, what is Article 10A of the Constitution of Pakistan about?"
)

print(response.content)