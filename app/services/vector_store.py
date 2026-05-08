from langchain_qdrant import QdrantVectorStore

from app.core.config import (
    QDRANT_URL,
    QDRANT_API_KEY
)


def store_documents(
    chunks,
    embedding_model
):

    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name="rag-notebooklm"
    )

    return vector_store