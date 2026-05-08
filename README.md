# 📘 RAG NotebookLM Clone

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=flat-square&logo=react)](https://react.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-RAG_Framework-black?style=flat-square)](https://www.langchain.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-red?style=flat-square)](https://qdrant.tech/)
[![Groq API](https://img.shields.io/badge/Powered%20by-Groq-orange?style=flat-square)](https://groq.com/)
[![Gemini Embeddings](https://img.shields.io/badge/Gemini-Embeddings-blueviolet?style=flat-square&logo=google)](https://ai.google.dev/)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?style=flat-square&logo=vercel)](https://vercel.com/)
[![Render](https://img.shields.io/badge/Backend-Render-46E3B7?style=flat-square&logo=render)](https://render.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Status: Active](https://img.shields.io/badge/Status-Active-success?style=flat-square)]()

---

# 🚀 Overview

A full-stack Retrieval-Augmented Generation (RAG) application inspired by Google NotebookLM.

Users can upload PDF documents and ask natural language questions about them.  
The system retrieves relevant chunks from the uploaded document and generates grounded AI responses using semantic search and LLM orchestration.

---

# ✨ Features

| Feature | Description |
|---|---|
| 📄 PDF Upload | Upload and process PDF documents |
| ✂️ Smart Chunking | Recursive chunk splitting with overlap |
| 🧠 Semantic Search | Meaning-based retrieval using embeddings |
| 🗂️ Vector Database | Qdrant vector storage |
| 🤖 Grounded AI Answers | Responses generated only from document context |
| 📚 Source Citations | Page-level references |
| 🌐 Full-Stack App | React frontend + FastAPI backend |
| ☁️ Cloud Deployment | Render + Vercel + Qdrant Cloud |

---

# 🛠️ Tech Stack

## Backend

| Technology | Purpose |
|---|---|
| Python | Backend language |
| FastAPI | API framework |
| LangChain | RAG orchestration |
| Groq API | LLM inference |
| Gemini Embeddings | Semantic embeddings |
| Qdrant | Vector database |
| PyPDF | PDF parsing |

---

## Frontend

| Technology | Purpose |
|---|---|
| React | Frontend UI |
| Vite | Frontend build tool |
| Axios | API communication |

---

## Deployment

| Service | Purpose |
|---|---|
| Render | Backend deployment |
| Vercel | Frontend deployment |
| Qdrant Cloud | Hosted vector database |

---

# 🧠 RAG Pipeline Architecture

```text
PDF Upload
     ↓
PDF Parsing
     ↓
Chunking
     ↓
Embeddings
     ↓
Qdrant Vector Storage
     ↓
Semantic Retrieval
     ↓
Groq LLM
     ↓
Grounded Answer
```

---

# 📂 Project Structure

```text
rag-notebooklm/
│
├── app/
│   ├── api/
│   │   ├── upload.py
│   │   └── chat.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── prompts.py
│   │
│   ├── services/
│   │   ├── pdf_loader.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   └── llm.py
│   │
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.jsx
│
├── uploads/
├── requirements.txt
├── .env
├── run.py
└── README.md
```

---

# ⚙️ How The System Works

| Step | Description |
|---|---|
| 1 | User uploads a PDF |
| 2 | PDF text is extracted |
| 3 | Text is split into chunks |
| 4 | Chunks are converted into embeddings |
| 5 | Embeddings stored in Qdrant |
| 6 | User asks a question |
| 7 | Relevant chunks retrieved semantically |
| 8 | Groq generates grounded answer |
| 9 | Response returned with citations |

---

# ✂️ Chunking Strategy

The application uses:

```python
RecursiveCharacterTextSplitter
```

Configuration:

```python
chunk_size = 500
chunk_overlap = 100
```

---

## Why Chunk Overlap Matters

Chunk overlap preserves semantic continuity between chunks.

### Example

```text
Chunk 1:
"Node.js debugging starts with..."

Chunk 2:
"...starts with breakpoints and Chrome DevTools"
```

This improves:
- retrieval quality
- contextual understanding
- answer grounding

---

# 🧠 Embeddings

The application uses:

```text
Gemini Embeddings
models/text-embedding-004
```

Embeddings convert text into numerical vector representations for semantic similarity search.

---

# 🗂️ Vector Database

The application uses:

```text
Qdrant Vector Database
```

Qdrant stores:
- embeddings
- chunk metadata
- page references

and performs nearest-neighbor semantic search.

---

# 🔍 Semantic Retrieval

When the user asks a question:

1. Question converted into embedding vector
2. Qdrant performs similarity search
3. Top relevant chunks retrieved
4. Chunks passed into Groq LLM

This enables meaning-based retrieval instead of keyword matching.

---

# 🤖 Grounded Answer Generation

Retrieved chunks are injected into a grounded system prompt.

The model is instructed to:

- answer ONLY from retrieved context
- avoid outside knowledge
- reduce hallucinations
- provide structured responses

---

# 📌 Example Workflow

```text
User Question:
"How does Node.js debugging work?"

        ↓

Retriever finds relevant chunks

        ↓

Groq generates grounded response

        ↓

Response returned with page citations
```

---

# 🔒 Hallucination Prevention

The system uses:

| Technique | Purpose |
|---|---|
| RAG Pipeline | Ground answers in retrieved context |
| Prompt Engineering | Restrict external knowledge |
| Semantic Retrieval | Improve relevance |
| Source Citations | Improve transparency |

If information does not exist in the document:

```text
"I could not find this information in the document."
```

---

# 🌐 API Endpoints

## Upload PDF

### Endpoint

```http
POST /upload
```

### Purpose

Uploads and indexes PDF documents.

---

## Chat With Document

### Endpoint

```http
POST /chat
```

### Request

```json
{
  "question": "Explain debugging in Node.js"
}
```

### Response

```json
{
  "answer": "...",
  "sources": [
    {
      "page": 12
    }
  ]
}
```

---

# 💻 Local Setup

## 1. Clone Repository

```bash
git clone YOUR_GITHUB_REPO
cd rag-notebooklm
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### Activate Environment

#### Linux / Mac

```bash
source venv/bin/activate
```

#### Windows

```powershell
venv\Scripts\activate
```

---

## 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Setup Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_groq_api_key

GOOGLE_API_KEY=your_gemini_api_key

QDRANT_URL=your_qdrant_url

QDRANT_API_KEY=your_qdrant_api_key
```

---

## 5. Run Backend

```bash
python run.py
```

Backend runs on:

```text
http://localhost:8000
```

---

## 6. Run Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# 📚 Key Concepts Learned

| Topic | Concepts |
|---|---|
| Backend Engineering | FastAPI, routing, APIs |
| RAG Systems | Retrieval-Augmented Generation |
| Embeddings | Semantic vector representations |
| Vector Databases | Qdrant similarity search |
| Prompt Engineering | Grounding and hallucination prevention |
| Full-Stack Development | React + FastAPI integration |
| Deployment | Render + Vercel workflows |

---

# 🚀 Future Improvements

| Improvement | Description |
|---|---|
| Multi-document Support | Chat across multiple PDFs |
| Streaming Responses | Real-time token streaming |
| Chat History | Persistent memory |
| Authentication | User login system |
| OCR Support | Scanned PDF support |
| Hybrid Search | BM25 + semantic search |
| Summarization | Auto document summaries |

---

# 🌐 Deployment

| Service | Link |
|---|---|
| Frontend | YOUR_VERCEL_LINK |
| Backend | YOUR_RENDER_LINK |
| GitHub Repository | YOUR_GITHUB_LINK |

---

# 📖 What This Project Demonstrates

This project demonstrates:

- End-to-end RAG implementation
- AI orchestration pipelines
- Semantic retrieval systems
- Vector database integration
- Prompt grounding techniques
- Full-stack AI engineering
- Cloud deployment workflows

---

# 🙌 Acknowledgements

Built using:

- LangChain
- FastAPI
- Groq
- Gemini Embeddings
- Qdrant
- React
- Vite

---

# ⭐ Final Note

This project was built to deeply understand:

- Retrieval-Augmented Generation (RAG)
- Semantic search systems
- Vector databases
- AI application engineering

Instead of simply calling LLM APIs, this project focuses on how modern AI systems are actually designed, grounded, and orchestrated in production environments.