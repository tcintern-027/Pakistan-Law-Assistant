# Pakistan Law Assistant — Project Memory

## Project

**Name:** Pakistan Law Assistant

**Type:** Domain-specific RAG legal information assistant

**Purpose:** Apply the complete RAG workflow to Pakistani legal documents.

## Current Status

Phase 0 — Project Foundation

The initial project structure and project documentation have been created.

## Technology Stack

### Backend

* Python
* FastAPI
* LangChain
* ChromaDB
* Pydantic

### AI

* Embedding model
* LLM API

### Frontend

* React
* Tailwind CSS

### Development

* Git
* GitHub
* Python virtual environment
* pytest

## Current Directory Structure

```text
Task 8 Pakistan Law Assistant/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── loaders.py
│   │   ├── splitter.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── prompt.py
│   │   ├── llm.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   ├── documents.py
│   │   │   └── health.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   └── document.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── rag_service.py
│   │       └── document_service.py
│   │
│   └── data/
│       ├── documents/
│       └── chroma_db/
│
├── frontend/
│
├── tests/
│   ├── __init__.py
│   └── test_rag.py
│
├── PRD.md
├── Architecture.md
├── Rules.md
├── Phases.md
├── Design.md
├── Memory.md
├── README.md
└── .gitignore
```

## Initial Legal Document Set

Planned:

1. Constitution of Pakistan
2. Pakistan Penal Code
3. Contract Act
4. PECA / relevant cybercrime legislation

## RAG Pipeline

```text
Legal Documents
      ↓
LangChain Loaders
      ↓
Text Splitting
      ↓
Embeddings
      ↓
ChromaDB
      ↓
Retriever
      ↓
Retrieved Context
      ↓
Prompt
      ↓
LLM
      ↓
Grounded Answer + Sources
```

## API Plan

Planned endpoints:

```text
GET  /health
POST /ask
```

Additional document-management endpoints will be added later.

## Important Constraints

* The assistant provides educational legal information.
* It is not a substitute for professional legal advice.
* Responses should be grounded in indexed documents.
* The system should acknowledge insufficient information.
* Sources should be shown whenever possible.
* API keys must never be committed to GitHub.
* Project dependencies should be installed inside the project virtual environment.

## Development History

### 2026-08-09

* Created project directory.
* Created backend directory structure.
* Created frontend directory.
* Created tests directory.
* Created initial project documentation files.
* Established initial architecture.
* Established development rules.
* Established project phases.
* Established initial UI design direction.

## Current Next Step

Set up the Python virtual environment and backend dependencies.

After dependency setup, update:

* `Phases.md`
* `Memory.md`

If architecture or technology decisions change, also update:

* `Architecture.md`
* `PRD.md`

If UI decisions change, update:

* `Design.md`

## Documentation Maintenance Rule

This file must be updated after every meaningful implementation milestone.

Record:

* What was implemented.
* Important decisions.
* Problems encountered.
* Solutions applied.
* Current project state.
* Exact next step.
