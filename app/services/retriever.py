from langchain_qdrant import QdrantVectorStore

from app.core.config import (
    QDRANT_URL,
    QDRANT_API_KEY
)


def retrieve_chunks(
    query,
    embedding_model,
    k=5
):

    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name="rag-notebooklm"
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )

    results = retriever.invoke(query)

    return results