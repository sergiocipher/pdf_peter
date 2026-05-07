from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embeddings import get_embedding_model
from app.services.retriever import retrieve_chunks

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    # user question
    query = request.question

    # embedding model
    embedding_model = get_embedding_model()

    # retrieve chunks
    results = retrieve_chunks(
        query=query,
        embedding_model=embedding_model
    )

    extracted_chunks = []

    for doc in results:
        extracted_chunks.append({
            "page_content": doc.page_content,
            "page_number": doc.metadata.get("page")
        })

    return {
        "question": query,
        "retrieved_chunks": extracted_chunks
    }