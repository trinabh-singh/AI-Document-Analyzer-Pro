# 📄 AI Document Analyzer Pro

A production-style **Retrieval-Augmented Generation (RAG)** system for intelligent PDF document analysis.

The application allows users to upload PDF documents, ask natural language questions, and receive grounded answers generated using Hybrid Retrieval, Cross-Encoder Reranking, and Large Language Models.

---

## ✨ Features

- 📄 Upload and analyze PDF documents
- 🔍 Hybrid Retrieval (Dense Embeddings + BM25)
- 🔄 Reciprocal Rank Fusion (RRF)
- 🎯 Cross Encoder Re-ranking
- 🤖 LLM-powered answer generation
- 📚 Source citations
- 📊 RAGAS evaluation dashboard
- 💬 Chat history
- 🗑️ Clear Chat functionality
- 🐳 Docker Compose deployment
- ⚡ FastAPI backend
- 🎨 Streamlit frontend
- 🗄️ Qdrant vector database

---

# 🏗️ System Architecture

```
                  PDF Upload
                       │
                       ▼
              Document Loader
                       │
                       ▼
                  Text Chunking
                       │
                       ▼
            Sentence Embeddings
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
    Dense Search                BM25 Search
         │                           │
         └─────────────┬─────────────┘
                       ▼
           Reciprocal Rank Fusion
                       ▼
          Cross Encoder Reranking
                       ▼
                  Top Context
                       ▼
                  LLM Response
                       ▼
               RAGAS Evaluation
```

---

# 🛠️ Tech Stack

### Backend

- FastAPI
- Python

### Frontend

- Streamlit

### Retrieval

- Sentence Transformers
- BM25
- Reciprocal Rank Fusion
- Cross Encoder

### Vector Database

- Qdrant

### Evaluation

- RAGAS

### Deployment

- Docker
- Docker Compose

---

# 📂 Project Structure

```text
AI-Document-Analyzer-Pro/

├── app/
│   ├── ingestion/
│   ├── retrieval/
│   ├── generation/
│   ├── evaluation/
│   ├── vector_database/
│   ├── frontend.py
│   ├── api.py
│   └── rag_pipeline.py
│
├── requirements/
│   ├── backend.txt
│   └── frontend.txt
│
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── .env.example
└── README.md
```

---

# 🚀 Getting Started

## Clone the repository

```bash
git clone https://github.com/<your-username>/AI-Document-Analyzer-Pro.git

cd AI-Document-Analyzer-Pro
```

---

## Configure environment variables

Create a `.env` file:

```env
OPENROUTER_API_KEY=YOUR_API_KEY

QDRANT_HOST=qdrant
QDRANT_PORT=6333

API_URL=http://backend:8000
```

---

## Run with Docker

```bash
docker compose up --build
```

Open:

Frontend

```
http://localhost:8501
```

Backend

```
http://localhost:8000/docs
```

Qdrant Dashboard

```
http://localhost:6333/dashboard
```

---

# 📊 RAG Pipeline

1. Upload PDF
2. Extract text
3. Chunk document
4. Generate embeddings
5. Store vectors in Qdrant
6. Perform Hybrid Retrieval
7. Fuse rankings using RRF
8. Re-rank using Cross Encoder
9. Generate answer using LLM
10. Evaluate answer using RAGAS

---


# Future Improvements

- Streaming responses
- Authentication
- Conversation export
- OCR support
- Multi-user support

---

# 👨‍💻 Author

**Trinabh Singh Thakur**

GitHub:
https://github.com/trinabh-singh

LinkedIn:
https://www.linkedin.com/in/trinabh-singh-thakur-4681793a1/

---

# ⭐ If you found this project useful, consider giving it a star!