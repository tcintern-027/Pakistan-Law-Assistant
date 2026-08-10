# Pakistan Law Assistant — Project Memory

## Project

**Name:** Pakistan Law Assistant

**Type:** Domain-specific RAG legal information assistant

**Purpose:** Apply the complete RAG workflow to Pakistani legal documents and provide grounded legal information with source and page-level citations.

---

## Current Status

**Phase 6 — LLM and RAG Service**

Phases 0–5 have been implemented and tested successfully.

The project currently has:

* A verified Pakistani legal document corpus.
* LangChain PDF document loading.
* Text splitting and chunk inspection.
* Hugging Face embeddings.
* Persistent ChromaDB vector storage.
* Semantic similarity retrieval.
* Hybrid legal-aware retrieval using semantic and lexical matching.
* Exact legal-reference matching for references such as `Article 10A` and `Section 302`.

The next implementation milestone is to build the **LLM and RAG answer-generation layer** using Groq.

---

# Technology Stack

## Backend

* Python
* FastAPI
* LangChain
* ChromaDB
* Pydantic

## AI

* Hugging Face Sentence Transformers
* `sentence-transformers/all-MiniLM-L6-v2`
* Groq LLM

## Frontend

* React
* Tailwind CSS

## Development

* Git
* GitHub
* Python virtual environment
* pytest

---

# Current Directory Structure

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

---

# Initial Legal Document Corpus

The initial corpus contains four Pakistani legal documents:

1. Constitution of Pakistan
2. Pakistan Penal Code
3. Contract Act, 1872
4. PECA / relevant cybercrime legislation

Documents are stored under:

```text
backend/data/documents/
```

Generated ChromaDB data is stored under:

```text
backend/data/chroma_db/
```

---

# Document Provenance

The Constitution PDF currently used in the project is the version marked:

```text
As modified upto the 21st October, 2024.
```

Project documentation must not claim that this Constitution PDF contains amendments through November 2025.

The document provenance is recorded in:

```text
backend/data/documents/SOURCES.md
```

---

# RAG Pipeline

The implemented and planned pipeline is:

```text
Legal Documents
      ↓
LangChain PDF Loaders
      ↓
Text Splitting
      ↓
Hugging Face Embeddings
      ↓
ChromaDB
      ↓
Hybrid Retriever
      ↓
Retrieved Legal Context
      ↓
Legal RAG Prompt
      ↓
Groq LLM
      ↓
Grounded Answer
      ↓
Sources + Page Citations + Disclaimer
```

---

# Phase 2 — Document Loading

## Completed

Implemented:

```text
backend/app/loaders.py
```

The loader uses LangChain `PyPDFLoader`.

The four legal PDFs were successfully loaded into LangChain `Document` objects.

Total loaded page-level documents:

```text
518
```

Metadata preservation was verified, including:

* Source filename
* Page number

Loader tests were successfully executed.

---

# Phase 3 — Text Splitting

## Completed

Implemented:

```text
backend/app/splitter.py
```

The project uses LangChain text splitters to divide page-level legal documents into retrieval-friendly chunks.

Chunking was tested and inspected manually.

The resulting chunks preserve document metadata such as:

* Source filename
* Page
* Chunk identifier/index

Important legal provisions were manually inspected after splitting.

For example, Article 10A of the Constitution was successfully found inside:

```text
Chunk ID: chunk_00048
```

with the relevant text:

```text
10A.
For the determination of his civil rights and obligations
or in any criminal charge against him a person shall be entitled
to a fair trial and due process.
```

This confirmed that important legal provisions were not lost during splitting.

---

# Phase 4 — Embeddings and ChromaDB

## Completed

Implemented:

```text
backend/app/embeddings.py
backend/app/vector_store.py
```

Initial embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

ChromaDB is configured as the persistent vector store.

Persistent location:

```text
backend/data/chroma_db/
```

Collection:

```text
pakistan_law_documents
```

The vector store uses the same embedding configuration for indexing and querying.

ChromaDB persistence and similarity retrieval were tested successfully.

Vector-store inspection confirmed that legal chunks from all four documents are available.

---

# Phase 5 — Retriever

## Completed

Implemented:

```text
backend/app/retriever.py
```

The retriever initially used semantic similarity search.

It was then improved into a hybrid legal-aware retrieval layer.

The current retriever combines:

1. Semantic similarity retrieval.
2. Exact legal-reference matching.
3. Important legal phrase matching.
4. Semantic ranking.
5. Lightweight document-quality penalties.

Legal references such as:

```text
Article 10A
Section 302
```

receive stronger lexical weighting.

Important legal phrases include examples such as:

```text
fair trial
due process
fundamental right
freedom of speech
freedom of expression
right to education
right to information
right to life
death penalty
life imprisonment
electronic crimes
cyber crime
criminal liability
private defence
bail
pre-arrest bail
post-arrest bail
```

Table-of-contents and very short chunks receive penalties to reduce irrelevant retrieval.

---

# Retrieval Testing

The retriever was tested with multiple legal queries.

Examples included:

```text
What does Article 10A say?
```

and queries relating to:

```text
fair trial
due process
private defence
kidnapping
rape
cybercrime
Pakistan Penal Code sections
Contract Act provisions
```

The tests successfully returned relevant legal documents and chunks.

Article 10A was specifically verified in the Constitution chunk:

```text
Source: Constitution of Pakistan.pdf
Page: 25
Chunk ID: chunk_00048
```

The retrieved content contained the actual Article 10A provision concerning:

```text
fair trial and due process
```

This confirms that the retrieval pipeline can locate an exact constitutional provision rather than relying only on semantically similar content.

---

# Retriever Bug and Resolution

During development, `retriever.py` temporarily contained an accidental self-import:

```python
from backend.app.retriever import retrieve_documents
```

This caused:

```text
ImportError:
cannot import name 'retrieve_documents' from partially initialized module
```

The self-import was removed and `retriever.py` was restored to the proper implementation.

The retriever test subsequently executed successfully.

---

# Current Phase — Phase 6: LLM and RAG Service

## Objective

Convert retrieved legal context into grounded natural-language answers using the Groq LLM.

The target pipeline is:

```text
User Question
      ↓
Hybrid Retriever
      ↓
Relevant Legal Chunks
      ↓
Legal RAG Prompt
      ↓
Groq LLM
      ↓
Grounded Legal Answer
      ↓
Source + Page Citations
      ↓
Legal Disclaimer
```

## Phase 6 Tasks

* [ ] Configure Groq LLM.
* [ ] Verify `langchain-groq`.
* [ ] Verify `GROQ_API_KEY` configuration.
* [ ] Create legal RAG prompt.
* [ ] Implement RAG service.
* [ ] Pass retrieved context to Groq.
* [ ] Generate grounded answers.
* [ ] Include source filename and page number.
* [ ] Handle insufficient context.
* [ ] Prevent unsupported legal claims.
* [ ] Add educational legal disclaimer.
* [ ] Test complete question → retrieval → answer pipeline.

---

# API Plan

Planned initial endpoints:

```text
GET  /health
POST /ask
```

Additional document-management endpoints will be implemented later.

FastAPI implementation begins after the core RAG service is working independently.

---

# Important Constraints

* The assistant provides educational legal information.
* It is not a substitute for professional legal advice.
* Responses should be grounded in indexed legal documents.
* The system should acknowledge when the indexed documents do not contain sufficient information.
* Sources should be shown whenever possible.
* Source filename and page metadata should be preserved.
* API keys must never be committed to GitHub.
* Backend dependencies must be installed inside the project virtual environment.
* Legal documents should come from reliable and authoritative sources whenever possible.
* Generated ChromaDB data should not be committed to Git.
* The LLM should not be allowed to fabricate legal provisions.
* Retrieval context should be explicitly provided to the LLM.
* Legal answers should distinguish between information found in the indexed documents and information that is unavailable.

---

# Development History

## 2026-08-09 — Project Foundation

* Created project directory.
* Created backend directory structure.
* Created frontend directory.
* Created tests directory.
* Created initial project documentation.
* Established initial architecture.
* Established development rules.
* Established project phases.
* Established initial UI design direction.

## 2026-08-09 — Phase 0 Completed

* Initialized Git repository.
* Created `main` branch.
* Created backend Python virtual environment.
* Added initial backend dependencies.
* Configured environment variable structure.
* Added `.gitignore`.
* Protected API keys and generated ChromaDB data from Git.
* Created initial foundation commit.
* Established development workflow for maintaining documentation after meaningful milestones.

## 2026-08-09 — Phase 1 Completed

* Collected the initial Pakistani legal document corpus.
* Added the Constitution of Pakistan.
* Added the Pakistan Penal Code.
* Added the Contract Act, 1872.
* Added PECA / relevant cybercrime legislation.
* Verified that the PDFs can be opened.
* Verified that text can be extracted.
* Added `SOURCES.md` for document provenance.
* Established that document source and metadata must be preserved throughout the RAG pipeline.

## 2026-08-10 — Phase 2 Completed

* Implemented `backend/app/loaders.py`.
* Added LangChain PDF loading using `PyPDFLoader`.
* Loaded four legal documents.
* Successfully converted the PDFs into LangChain `Document` objects.
* Loaded 518 page-level documents.
* Preserved source metadata.
* Preserved page metadata.
* Added loader tests.
* Successfully executed loader tests.
* Confirmed legal text extraction.

## 2026-08-10 — Phase 3 Completed

* Implemented text splitting.
* Generated retrieval-friendly legal chunks.
* Preserved source and page metadata.
* Inspected generated chunks.
* Verified that Article 10A remained intact within a chunk.
* Confirmed that legal provisions can be located after chunking.

## 2026-08-10 — Phase 4 Completed

* Implemented the embeddings module.
* Configured `sentence-transformers/all-MiniLM-L6-v2`.
* Implemented persistent ChromaDB vector storage.
* Created the `pakistan_law_documents` collection.
* Indexed legal chunks.
* Verified stored vectors.
* Tested semantic similarity search.

## 2026-08-10 — Phase 5 Completed

* Implemented semantic retrieval.
* Improved retrieval with lexical/legal-reference matching.
* Added exact matching for Article/Section references.
* Added important legal phrase matching.
* Added lightweight penalties for table-of-contents and short chunks.
* Tested retrieval against multiple legal questions.
* Verified Article 10A retrieval.
* Fixed accidental circular/self-import in `retriever.py`.
* Successfully executed `test_retriever`.

---

# Current State

The project has completed the ingestion and retrieval portion of the RAG pipeline.

The current working pipeline is:

```text
PDF Documents
      ↓
PyPDFLoader
      ↓
Text Splitting
      ↓
Hugging Face Embeddings
      ↓
ChromaDB
      ↓
Hybrid Retriever
      ↓
Relevant Legal Chunks
```

The missing component is:

```text
Relevant Legal Chunks
      ↓
Groq LLM
      ↓
Grounded Legal Answer
```

---

# Exact Next Step

**Begin Phase 6 — LLM and RAG Service.**

First:

1. Verify the Groq LangChain package.
2. Verify the `GROQ_API_KEY` environment variable.
3. Implement `backend/app/llm.py`.
4. Implement/update `backend/app/prompt.py`.
5. Implement `backend/app/services/rag_service.py`.
6. Create a standalone RAG test.
7. Test questions such as:

```text
What does Article 10A say?
What is Section 302 of the Pakistan Penal Code?
What does PECA say about real-time collection of information?
```

The Phase 6 implementation must be completed and tested before beginning Phase 7 — FastAPI.

---

# Documentation Maintenance Rule

This file must be updated after every meaningful implementation milestone.

Record:

* What was implemented.
* Important technical decisions.
* Problems encountered.
* Solutions applied.
* Current project state.
* Current phase.
* Completed tasks.
* Exact next step.

The other project documentation should also be updated when relevant:

* `PRD.md` → requirements and features
* `Architecture.md` → architecture and technical components
* `Rules.md` → project/development rules
* `Phases.md` → roadmap and progress
* `Design.md` → UI/UX decisions
* `Memory.md` → implementation history and current state
