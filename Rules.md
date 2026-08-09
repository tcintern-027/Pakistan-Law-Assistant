# Pakistan Law Assistant — Project Rules

## 1. General Development Rules

1. Build the project incrementally.
2. Do not skip foundational steps.
3. Do not introduce unnecessary technologies.
4. Keep the architecture modular.
5. Prefer simple, maintainable implementations.
6. Do not duplicate functionality.
7. Do not rewrite working components without a clear reason.

## 2. RAG Rules

1. Answers must be grounded in retrieved legal documents.
2. The LLM must not be instructed to invent legal provisions.
3. Retrieved context must be supplied to the LLM.
4. Sources should be returned with answers whenever possible.
5. If the retrieved documents do not contain sufficient information, the system must say so.
6. Retrieval quality should be tested before adding unnecessary complexity.
7. Document metadata must be preserved whenever possible.

## 3. Legal Safety Rules

The application is an educational legal information assistant.

Every user-facing experience must make clear that:

> This application provides legal information for educational purposes only. It is not a substitute for professional legal advice.

The system must not present generated information as guaranteed legal advice.

The system should avoid making unsupported conclusions about a user's specific legal situation.

## 4. Document Rules

Initial documents should come from reliable sources.

Initial collection:

* Constitution of Pakistan
* Pakistan Penal Code
* Contract Act
* PECA / relevant cybercrime legislation

Documents should be stored under:

```text
backend/data/documents/
```

Generated ChromaDB data should be stored under:

```text
backend/data/chroma_db/
```

## 5. Code Rules

* Use Python type hints where practical.
* Use Pydantic models for API data.
* Keep API routes thin.
* Put RAG logic inside services/modules.
* Keep configuration centralized.
* Never hardcode API keys.
* Store secrets in `.env`.
* Provide `.env.example` placeholders.
* Use meaningful function and variable names.
* Avoid unnecessary global state.

## 6. Git Rules

Commits should be small and meaningful.

Preferred format:

```text
feat: add legal document loader
feat: implement document chunking
feat: add ChromaDB vector store
feat: implement legal retriever
feat: add FastAPI ask endpoint
fix: handle missing retrieval context
docs: update architecture
refactor: separate RAG service
```

Do not use vague commits such as:

```text
update
changes
stuff
final
working
```

## 7. Testing Rules

Important RAG components should be tested independently where practical.

Testing should eventually cover:

* Document loading
* Text splitting
* Embeddings/vector storage
* Retrieval
* RAG responses
* API endpoints

## 8. Environment Rules

Development should use the project's virtual environment.

Do not install project dependencies globally when the project virtual environment is available.

Secrets must never be committed to GitHub.

## 9. Frontend Rules

The frontend should:

* Use React.
* Use Tailwind CSS.
* Be responsive.
* Clearly display sources.
* Clearly display the legal disclaimer.
* Handle loading and API errors.
* Never expose API keys.

## 10. Change Management Rule

After every meaningful project step, update the appropriate project documentation.

Possible documentation updates:

* `PRD.md` — requirements/features change.
* `Architecture.md` — architecture or component change.
* `Rules.md` — development rule/process change.
* `Phases.md` — progress or milestone change.
* `Design.md` — UI/UX change.
* `Memory.md` — important implementation decisions and current state.

Documentation must remain consistent with the actual codebase.
