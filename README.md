# Pakistan Law Assistant

An AI-powered legal question-answering system built specifically for Pakistani legal documents. The application combines Retrieval-Augmented Generation (RAG), hybrid document retrieval, semantic embeddings, ChromaDB, and Groq-powered language models to provide grounded answers with legal source references.

## Overview

Pakistan Law Assistant enables users to ask natural-language questions about Pakistani law and receive answers grounded in a curated collection of legal documents.

The system retrieves relevant legal passages from the indexed document collection, provides them as context to a language model, and generates a source-aware response.

The project also includes an evaluation pipeline for measuring answer quality, relevance, and groundedness across a 15-case legal evaluation dataset.

## Key Features

- AI-powered legal question answering
- Retrieval-Augmented Generation (RAG)
- Hybrid legal document retrieval
- Semantic vector search using embeddings
- ChromaDB vector database
- Groq-powered LLM responses
- Support for Pakistani legal documents
- Source-aware responses
- Document and page references
- Chunk-level metadata tracking
- FastAPI backend
- React + TypeScript frontend
- Tailwind CSS interface
- REST API architecture
- Input validation with Pydantic
- Health-check endpoint
- Environment-based configuration
- LLM-as-a-Judge evaluation
- Correctness, relevance, and groundedness metrics
- 15-case evaluation dataset
- Hallucination and unknown-query testing
- Retrieval failure analysis
- Before/after evaluation comparison

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- LangChain
- ChromaDB
- Hugging Face Embeddings
- Groq
- Pydantic

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Lucide React
- JavaScript Fetch API

### AI / RAG

- Retrieval-Augmented Generation
- Hybrid Retrieval
- Semantic Embeddings
- Vector Search
- Document Chunking
- Metadata-aware Retrieval
- Grounded Prompting
- Groq LLM

### Evaluation

- LangChain evaluation pipeline
- LLM-as-a-Judge
- Evaluation dataset
- Correctness
- Relevance
- Groundedness
- Failure analysis
- Before/after comparison

## Architecture

    React Frontend
          |
          | HTTP / REST API
          v
    FastAPI Backend
          |
          v
    RAG Service
          |
          +------------------+
          |                  |
          v                  v
    Hybrid Retriever     Groq LLM
          |
          v
       ChromaDB

## RAG Pipeline

    User Question
          |
          v
    FastAPI API
          |
          v
    RAG Service
          |
          v
    Hybrid Retriever
          |
          v
    Relevant Legal Chunks
          |
          v
    Legal RAG Prompt
          |
          v
    Groq LLM
          |
          v
    Grounded Legal Answer
          |
          v
    Sources + Metadata
          |
          v
    React Frontend

## Project Structure

    Pakistan Law Assistant/
    |
    +-- backend/
    |   +-- app/
    |   |   +-- routes/
    |   |   |   +-- __init__.py
    |   |   |   +-- chat.py
    |   |   |   +-- documents.py
    |   |   |   +-- health.py
    |   |   |
    |   |   +-- schemas/
    |   |   |   +-- __init__.py
    |   |   |   +-- chat.py
    |   |   |   +-- document.py
    |   |   |
    |   |   +-- services/
    |   |   |   +-- __init__.py
    |   |   |   +-- document_service.py
    |   |   |   +-- rag_service.py
    |   |   |
    |   |   +-- __init__.py
    |   |   +-- main.py
    |   |   +-- config.py
    |   |   +-- embeddings.py
    |   |   +-- index_documents.py
    |   |   +-- llm.py
    |   |   +-- loaders.py
    |   |   +-- prompt.py
    |   |   +-- retriever.py
    |   |   +-- splitter.py
    |   |   +-- vector_store.py
    |   |
    |   +-- data/
    |   +-- venv/
    |   +-- requirements.txt
    |
    +-- evaluation/
    |   +-- evaluation_dataset.json
    |   +-- results.json
    |   +-- evaluation_report.json
    |   +-- run_evaluation.py
    |   +-- evaluate_results.py
    |
    +-- frontend/
    |   +-- src/
    |   |   +-- components/
    |   |   +-- services/
    |   |   +-- types/
    |   |   +-- ...
    |   +-- public/
    |   +-- package.json
    |   +-- vite.config.ts
    |   +-- tsconfig.json
    |
    +-- .env.example
    +-- .gitignore
    +-- README.md

## Legal Documents

The current knowledge base contains:

- Constitution of Pakistan
- Pakistan Penal Code
- Contract Act, 1872
- Prevention of Electronic Crimes Act (PECA)

## Backend Components

### Document Loading

Legal PDF documents are loaded and prepared for indexing.

### Text Splitting

Documents are divided into manageable chunks before embedding. Chunk metadata is preserved so retrieved information can be traced back to its original document and page.

### Embeddings

Legal document chunks are converted into vector representations using Hugging Face embeddings.

These vectors allow semantically related legal passages to be retrieved even when the wording of the user's question differs from the original document.

### ChromaDB

ChromaDB stores document embeddings and associated metadata.

Important metadata includes:

    source_file
    page
    chunk_id
    chunk_index

This allows retrieved content to be traced back to its original legal document.

### Hybrid Retrieval

The retrieval layer combines semantic retrieval with legal-reference and lexical matching.

The retrieval process:

1. Performs semantic retrieval from ChromaDB.
2. Detects explicit references such as Article 10A and Section 302.
3. Retrieves documents containing those references.
4. Merges semantic and exact-reference candidates.
5. Calculates lexical relevance.
6. Applies semantic ranking.
7. Applies document-quality penalties.
8. Returns the highest-ranked legal documents.

This improves retrieval for highly specific legal questions where semantic similarity alone may miss the exact legal provision.

### RAG Service

The RAG service connects retrieval with the language model:

    Question
       |
       v
    Retrieve Documents
       |
       v
    Format Legal Context
       |
       v
    Build Legal Prompt
       |
       v
    Invoke Groq LLM
       |
       v
    Generate Answer
       |
       v
    Return Sources

### Legal Prompting

The application uses a dedicated legal RAG prompt that instructs the model to generate answers based on retrieved legal context.

The response is designed to remain grounded in the provided legal documents and includes source information and an educational-use disclaimer.

## API

### Health Check

    GET /health

Example response:

    {
      "status": "healthy",
      "service": "Pakistan Law Assistant"
    }

### Ask a Legal Question

    POST /ask

Example request:

    {
      "question": "What does Article 10A of the Constitution of Pakistan provide?"
    }

Example response:

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

## Frontend

The frontend is built using React and TypeScript with Vite.

Tailwind CSS is used for styling and Lucide React is used for interface icons.

The frontend communicates with the FastAPI backend through REST API requests.

    React UI
       |
       +-- Question Input
       |
       +-- API Request
       |
       +-- Answer Rendering
       |
       +-- Source References
               |
               v
           FastAPI /ask

## Evaluation

A dedicated evaluation pipeline was created to measure whether the RAG system produces high-quality legal answers.

### Evaluation Dataset

The evaluation dataset contains 15 test cases covering:

- Directly answerable questions
- Constitutional articles
- Pakistan Penal Code sections
- PECA questions
- Contract Act questions
- Multi-document questions
- Privacy and digital information
- Unknown legal references
- Fictional laws
- Hallucination and abstention cases

Example questions:

    What does Article 10A of the Constitution of Pakistan provide?

    What is Section 302 of the Pakistan Penal Code?

    What does PECA say about real-time collection of information?

    How do PECA and the Constitution address privacy and digital information?

    What does Pakistani law say about a hypothetical offence created by a fictional law called the Digital Crimes Act 2026?

    What does the Pakistan Penal Code say about a fictional Section 9999?

### Evaluation Metrics

The evaluation uses an LLM-as-a-Judge approach to measure:

- Correctness — whether the answer correctly addresses the expected legal information.
- Relevance — whether the answer directly addresses the question.
- Groundedness — whether the answer is supported by the retrieved legal context.

### Running the Evaluation

Run the RAG system against all 15 evaluation cases:

    python evaluation\run_evaluation.py

Results are saved to:

    evaluation/results.json

Evaluate the generated results:

    python evaluation\evaluate_results.py

The evaluation report is saved to:

    evaluation/evaluation_report.json

### Evaluation Results

The evaluation was run before and after improving the retrieval layer.

| Metric | Initial | Final |
|---|---:|---:|
| Test Cases | 15 | 15 |
| Correctness | 68.07% | 76.13% |
| Relevance | 86.40% | 88.20% |
| Groundedness | 92.40% | 82.07% |

### Issues Identified

The evaluation process identified several issues:

- Semantic retrieval could miss highly specific legal references.
- Some multi-document questions did not initially retrieve the most useful context.
- Questions involving fictional laws or sections required careful handling to prevent hallucination.
- Groq API rate limits occasionally interrupted evaluation runs.

### Improvement Implemented

The retrieval layer was improved from a primarily semantic approach to a hybrid retrieval strategy.

The updated system combines:

    Semantic Retrieval
            +
    Exact Legal Reference Retrieval
            +
    Lexical Matching
            +
    Semantic Reranking
            +
    Document Quality Penalties

Explicit references such as Article 10A and Section 302 are detected directly from the user query and used during retrieval and ranking.

This produced the following improvement:

    Correctness:   68.07% -> 76.13%
    Relevance:     86.40% -> 88.20%
    Groundedness:  92.40% -> 82.07%

## Example Legal Queries

    What does Article 10A of the Constitution of Pakistan provide?

    What is Section 302 of the Pakistan Penal Code?

    What does PECA say about real-time collection of information?

    What fundamental right is protected by Article 14 of the Constitution of Pakistan?

    What is a contract under the Contract Act 1872?

The system returns a generated legal explanation together with document and page-level source information.

## Local Development

### Backend

Navigate to the project directory:

    cd "C:\Internship Tasks\Task 8 Pakistan Law Assistant"

Activate the backend virtual environment:

    .\backend\venv\Scripts\Activate.ps1

Start the FastAPI server:

    python -m uvicorn backend.app.main:app --reload

The backend runs at:

    http://127.0.0.1:8000

### Frontend

Open another PowerShell window:

    cd "C:\Internship Tasks\Task 8 Pakistan Law Assistant\frontend"

Install dependencies:

    npm install

Start the development server:

    npm run dev

The frontend runs at:

    http://localhost:5173

## Production Build

From the frontend directory:

    npm run build

The production build is generated in:

    frontend/dist/

## Environment Variables

Create a .env file based on .env.example.

Example:

    GROQ_API_KEY=your_groq_api_key
    HF_TOKEN=your_huggingface_token

Sensitive credentials should never be committed to Git.

## Testing

The project includes tests for major RAG components, including:

- Embeddings
- Text splitting
- Vector storage
- Retrieval
- Hybrid retrieval
- LLM integration
- RAG service

Run the tests with:

    python -m pytest

## Legal Disclaimer

Pakistan Law Assistant is intended for educational and informational purposes only.

Generated responses should not be treated as a substitute for professional legal advice, legal representation, or consultation with a qualified lawyer.

## Development Philosophy

The project emphasizes:

- Modular architecture
- Separation of concerns
- Source-grounded generation
- Traceable legal context
- Hybrid retrieval
- Systematic evaluation
- Failure analysis
- Measurable improvements
- Reusable backend services
- Clean API boundaries
- Maintainable project structure

## License

This project is developed as an educational and portfolio project.
