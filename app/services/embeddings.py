# from langchain_huggingface import HuggingFaceEmbeddings

# def get_embedding_model():
    
#     embedding = HuggingFaceEmbeddings(
#         model_name = "sentence-transformers/all-MiniLM-L6-v2"
#     )

#     return embedding

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import GOOGLE_API_KEY


def get_embedding_model():

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GOOGLE_API_KEY
    )

    return embeddings