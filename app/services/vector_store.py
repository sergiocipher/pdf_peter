from langchain_qdrant import QdrantVectorStore


def store_documents(chunks, embedding_model ):

    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        url="http://localhost:6333",
        collection_name="rag-notebooklm"
    )

    return vector_store
