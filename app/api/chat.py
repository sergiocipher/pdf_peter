from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embeddings import get_embedding_model
from app.services.retriever import retrieve_chunks
from app.services.llm import generate_answer

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    query = request.question

    # embedding model
    embedding_model = get_embedding_model()

    # retrieve relevant chunks
    retrieved_docs = retrieve_chunks(
        query=query,
        embedding_model=embedding_model
    )

    # generate grounded answer
    answer = generate_answer(
        question=query,
        retrieved_docs=retrieved_docs
    )

    sources = []

    for doc in retrieved_docs:
        sources.append({
            "page": doc.metadata.get("page")
        })

    return {
        "question": query,
        "answer": answer,
        "sources": sources
    }