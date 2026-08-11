# Pakistan Law Assistant

An AI-powered legal question-answering system built specifically for Pakistani legal documents. The application combines Retrieval-Augmented Generation (RAG), hybrid document retrieval, semantic embeddings, ChromaDB, and Groq-powered language models to provide grounded answers with legal source references.

## Overview

Pakistan Law Assistant enables users to ask natural-language questions about Pakistani law and receive answers grounded in a curated collection of legal documents.

The system retrieves relevant legal passages from the indexed document collection, provides them as context to a language model, and generates a source-aware response.

The project is designed around a modular architecture that separates document processing, retrieval, LLM interaction, API services, and the React frontend.

## Key Features

* AI-powered legal question answering
* Retrieval-Augmented Generation (RAG)
* Hybrid legal document retrieval
* Semantic vector search using embeddings
* ChromaDB vector database
* Groq-powered LLM responses
* Support for Pakistani legal documents
* Source-aware responses
* Document and page references
* Chunk-level metadata tracking
* FastAPI backend
* React + TypeScript frontend
* Tailwind CSS interface
* Lucide React icons
* REST API architecture
* Input validation with Pydantic
* Health-check endpoint
* Environment-based configuration
* Modular backend service architecture

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn
* LangChain
* ChromaDB
* Hugging Face Embeddings
* Groq
* Pydantic

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* Lucide React
* JavaScript Fetch API

### AI / RAG

* Retrieval-Augmented Generation
* Hybrid Retrieval
* Semantic Embeddings
* Vector Search
* Document Chunking
* Metadata-aware Retrieval
* Grounded Prompting
* Groq LLM

## Architecture

The application follows a layered architecture:

```text
┌───────────────────────────────┐
│        React Frontend         │
│      React + TypeScript       │
│        Tailwind CSS           │
└───────────────┬───────────────┘
                │
                │ HTTP / REST API
                ▼
┌───────────────────────────────┐
│        FastAPI Backend        │
│                               │
│  API Routes / Validation      │
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│          RAG Service          │
│                               │
│ Question → Retrieval → Prompt │
│              → LLM            │
└───────────────┬───────────────┘
                │
        ┌───────┴────────┐
        ▼                ▼
┌───────────────┐ ┌───────────────┐
│ Hybrid        │ │ Groq LLM      │
│ Retriever     │ │               │
└───────┬───────┘ └───────────────┘
        │
        ▼
┌───────────────────────────────┐
│           ChromaDB            │
│      Vector Document Store     │
└───────────────────────────────┘
```

## RAG Pipeline

A typical question follows this pipeline:

```text
User Question
      │
      ▼
FastAPI API
      │
      ▼
RAG Service
      │
      ▼
Hybrid Retriever
      │
      ▼
Relevant Legal Chunks
      │
      ▼
Legal RAG Prompt
      │
      ▼
Groq LLM
      │
      ▼
Grounded Legal Answer
      │
      ▼
Sources + Metadata
      │
      ▼
React Frontend
```

## Project Structure

```text
Pakistan Law Assistant/
│
├── backend/
│   ├── app/
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
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── document_service.py
│   │   │   └── rag_service.py
│   │   │
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── embeddings.py
│   │   ├── index_documents.py
│   │   ├── llm.py
│   │   ├── loaders.py
│   │   ├── prompt.py
│   │   ├── retriever.py
│   │   ├── splitter.py
│   │   └── vector_store.py
│   │
│   ├── data/
│   ├── venv/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── types/
│   │   └── ...
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── .env.example
├── .gitignore
└── README.md
```

## Backend Components

### Document Loaders

The document processing layer loads legal documents and prepares them for indexing.

Supported document formats include:

* PDF
* TXT
* Markdown

### Text Splitting

Documents are divided into manageable chunks before embedding.

The project uses configurable text-splitting strategies to preserve useful context while keeping chunks suitable for semantic retrieval.

### Embeddings

Legal document chunks are converted into vector representations using Hugging Face embedding models.

These vectors allow semantically related legal passages to be retrieved even when the wording of the user's question differs from the original document.

### ChromaDB

ChromaDB is used as the vector database for storing document embeddings and associated metadata.

Metadata includes information such as:

```text
source_file
page
chunk_id
chunk_index
```

This enables retrieved content to be traced back to its original legal document.

### Hybrid Retrieval

The retrieval layer combines retrieval strategies to improve the relevance of legal context returned for a query.

Retrieved documents are ranked and passed into the RAG service for answer generation.

### RAG Service

The central RAG workflow is implemented through the RAG service:

```text
Question
   ↓
Retrieve Documents
   ↓
Format Legal Context
   ↓
Build Legal Prompt
   ↓
Invoke Groq LLM
   ↓
Generate Answer
   ↓
Return Sources
```

### Legal Prompting

The application uses a dedicated legal RAG prompt that instructs the model to generate answers based on the retrieved legal context.

The response format includes legal grounding and a general educational-use disclaimer.

## API

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "Pakistan Law Assistant"
}
```

### Ask a Legal Question

```http
POST /ask
```

Request:

```json
{
  "question": "What does Article 10A of the Constitution of Pakistan provide?"
}
```

Response:

```json
{
  "question": "What does Article 10A of the Constitution of Pakistan provide?",
  "answer": "Article 10A provides for the right to a fair trial...",
  "sources": [
    {
      "source": "Constitution of Pakistan.pdf",
      "page": 4,
      "chunk_id": "chunk_00003",
      "chunk_index": 0
    }
  ]
}
```

## Frontend

The frontend is built with React and TypeScript using Vite.

Tailwind CSS provides the styling system, while Lucide React provides reusable interface icons.

The frontend communicates with the FastAPI backend through REST API requests.

```text
React UI
   │
   ├── Question Input
   │
   ├── API Request
   │
   ├── Answer Rendering
   │
   └── Source References
          │
          ▼
      FastAPI /ask
```

## Example Legal Queries

The system can be queried with questions such as:

```text
What does Article 10A of the Constitution of Pakistan provide?

What is Section 302 of the Pakistan Penal Code?

What does PECA say about real-time collection of information?
```

The response includes the generated legal explanation together with document and page-level source information.

## Local Development

### Backend

Navigate to the project directory:

```powershell
cd "C:\Internship Tasks\Task 8 Pakistan Law Assistant"
```

Activate the backend virtual environment:

```powershell
.\backend\venv\Scripts\Activate.ps1
```

Start FastAPI:

```powershell
python -m uvicorn backend.app.main:app --reload
```

The backend runs at:

```text
http://127.0.0.1:8000
```

### Frontend

Open another PowerShell window:

```powershell
cd "C:\Internship Tasks\Task 8 Pakistan Law Assistant\frontend"
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend runs at:

```text
http://localhost:5173
```

## Production Build

From the frontend directory:

```powershell
npm run build
```

The Vite production build is generated in:

```text
frontend/dist/
```

## Environment Variables

Configure the required API credentials through environment variables.

Example:

```env
GROQ_API_KEY=your_groq_api_key
HF_TOKEN=your_huggingface_token
```

Sensitive credentials should be kept in `.env` and excluded from version control.

## Testing

The backend includes focused test modules for the major RAG components, including:

* Embeddings
* Text splitting
* Vector storage
* Retrieval
* Hybrid retrieval
* LLM integration
* RAG service

Example:

```powershell
python -m pytest
```

## Legal Disclaimer

Pakistan Law Assistant is intended for educational and informational purposes. Generated responses should not be treated as a substitute for professional legal advice, legal representation, or consultation with a qualified lawyer.

## Development Philosophy

The project emphasizes:

* Modular architecture
* Separation of concerns
* Source-grounded generation
* Traceable legal context
* Reusable backend services
* Type-safe frontend development
* Clean API boundaries
* Maintainable project structure
* Reproducible development environments

## License

This project is developed as an educational and portfolio project.
