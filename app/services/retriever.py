import logging
from langchain_qdrant import QdrantVectorStore

from app.core.config import (
    QDRANT_URL,
    QDRANT_API_KEY
)

logger = logging.getLogger(__name__)

COLLECTION_NAME = "rag-notebooklm"


def retrieve_chunks(
    query,
    embedding_model,
    k=5
):
    logger.info(
        f"Retrieving top-{k} chunks for query: '{query[:80]}...'"
    )

    try:
        vector_store = QdrantVectorStore.from_existing_collection(
            embedding=embedding_model,
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            collection_name=COLLECTION_NAME
        )

        retriever = vector_store.as_retriever(
            search_kwargs={"k": k}
        )

        results = retriever.invoke(query)

        logger.info(f"✅ Retrieved {len(results)} chunks")
        for i, doc in enumerate(results):
            page = doc.metadata.get("page", "?")
            logger.debug(f"  Chunk {i+1}: page {page}, {len(doc.page_content)} chars")

        return results

    except Exception as e:
        logger.error(f"❌ Retrieval failed: {e}")
        raise