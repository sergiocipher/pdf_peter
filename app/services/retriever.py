from langchain_qdrant import QdrantVectorStore


def retrieve_chunks(query,embedding_model):

    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        url="http://localhost:6333",
        collection_name="rag-notebooklm"
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    results = retriever.invoke(query)

    return results