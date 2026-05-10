import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.embeddings import get_embedding_model
from app.services.retriever import retrieve_chunks
from app.services.llm import generate_answer

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


# NOTE: Using `def` (not `async def`) so FastAPI runs this in a threadpool.
# This prevents blocking the event loop during synchronous embedding,
# Qdrant search, and Groq API calls.
@router.post("/chat")
def chat(request: ChatRequest):

    query = request.question
    logger.info(f"💬 Chat request: '{query[:80]}'")

    try:
        # embedding model
        embedding_model = get_embedding_model()

        # retrieve relevant chunks
        retrieved_docs = retrieve_chunks(
            query=query,
            embedding_model=embedding_model
        )
        logger.info(f"  Retrieved {len(retrieved_docs)} chunks")

        if not retrieved_docs:
            logger.warning("  ⚠️ No chunks retrieved — answer may be empty")

        # generate grounded answer
        answer = generate_answer(
            question=query,
            retrieved_docs=retrieved_docs
        )
        logger.info(f"  Answer generated ({len(answer)} chars)")

        sources = []
        seen_pages = set()

        for doc in retrieved_docs:
            page = doc.metadata.get("page")
            if page not in seen_pages:
                seen_pages.add(page)
                sources.append({
                    "page": page
                })

        return {
            "question": query,
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        logger.error(f"❌ Chat pipeline failed: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )