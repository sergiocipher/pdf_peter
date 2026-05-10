import logging
from langchain_qdrant import QdrantVectorStore

from app.core.config import (
    QDRANT_URL,
    QDRANT_API_KEY
)

logger = logging.getLogger(__name__)

COLLECTION_NAME = "rag-notebooklm"


def store_documents(
    chunks,
    embedding_model
):
    logger.info(
        f"Storing {len(chunks)} chunks in Qdrant collection '{COLLECTION_NAME}'"
    )

    try:
        vector_store = QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embedding_model,
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            collection_name=COLLECTION_NAME
        )

        logger.info(f"✅ Successfully stored {len(chunks)} chunks in Qdrant")
        return vector_store

    except Exception as e:
        logger.error(f"❌ Failed to store documents in Qdrant: {e}")
        raise