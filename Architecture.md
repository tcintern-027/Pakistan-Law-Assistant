# Pakistan Law Assistant — Architecture

## 1. Architecture Overview

The application follows a modular full-stack RAG architecture.

```text
                    ┌──────────────────────┐
                    │   React Frontend     │
                    │   + Tailwind CSS     │
                    └──────────┬───────────┘
                               │ HTTP
                               ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │    RAG Service       │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
          Retriever        Prompt          LLM
                │
                ▼
             ChromaDB
                │
                ▼
          Legal Documents
```

## 2. Backend Architecture

The backend is divided into several responsibilities.

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── loaders.py
│   ├── splitter.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── prompt.py
│   ├── llm.py
│   │
│   ├── routes/
│   │   ├── chat.py
│   │   ├── documents.py
│   │   └── health.py
│   │
│   ├── schemas/
│   │   ├── chat.py
│   │   └── document.py
│   │
│   └── services/
│       ├── rag_service.py
│       └── document_service.py
│
└── data/
    ├── documents/
    └── chroma_db/
```

## 3. RAG Ingestion Pipeline

```text
Legal Document
      ↓
LangChain Loader
      ↓
Document Objects
      ↓
Text Splitter
      ↓
Document Chunks
      ↓
Embedding Model
      ↓
Vector Embeddings
      ↓
ChromaDB
```

## 4. Query Pipeline

```text
User Question
      ↓
FastAPI /ask
      ↓
RAG Service
      ↓
Query Embedding
      ↓
ChromaDB Retriever
      ↓
Relevant Legal Chunks
      ↓
Prompt Construction
      ↓
LLM
      ↓
Grounded Answer + Sources
      ↓
FastAPI Response
      ↓
React UI
```

## 5. Component Responsibilities

### `loaders.py`

Responsible for loading supported document formats.

### `splitter.py`

Responsible for converting loaded documents into retrieval-friendly chunks.

### `embeddings.py`

Responsible for embedding configuration.

### `vector_store.py`

Responsible for ChromaDB initialization and persistence.

### `retriever.py`

Responsible for similarity-based retrieval.

### `prompt.py`

Contains the instructions that constrain the LLM to retrieved legal context.

### `llm.py`

Contains LLM configuration and initialization.

### `rag_service.py`

Coordinates the complete question-answering pipeline.

### `document_service.py`

Coordinates document ingestion and indexing.

### `routes/`

Contains FastAPI HTTP endpoints.

### `schemas/`

Contains request and response validation models.

## 6. Data Flow

Documents are processed during ingestion and persisted in ChromaDB.

User questions do not directly query the LLM.

Instead:

```text
Question → Retrieval → Context → LLM → Answer
```

This ensures the generated response is grounded in the indexed documents.

## 7. Metadata

Each indexed chunk should retain useful metadata where available, including:

* Source filename
* Document title
* Page number
* Section information
* Chunk identifier

This metadata will later be used for source citations.

## 8. Deployment Architecture

The intended deployment architecture is:

```text
User
 │
 ▼
React Frontend
 │
 │ HTTPS
 ▼
Deployed FastAPI Backend
 │
 ├── ChromaDB
 ├── Embedding Model/API
 └── LLM API
```

The frontend must use the deployed backend URL rather than `localhost` in production.

## 9. Architectural Principles

* Keep ingestion separate from retrieval.
* Keep business logic outside API routes.
* Use environment variables for secrets.
* Preserve document metadata.
* Keep RAG components independently testable.
* Avoid coupling the frontend to internal backend implementation.
* Prefer modular services over a monolithic implementation.
