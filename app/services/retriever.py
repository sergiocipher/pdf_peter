from langchain_qdrant import QdrantVectorStore


def retrieve_chunks(query,embedding_model , k=5):

    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        url="http://localhost:6333",
        collection_name="rag-notebooklm"
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": k}
    )

    results = retriever.invoke(query)

    return results