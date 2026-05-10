# from langchain_huggingface import HuggingFaceEmbeddings

# def get_embedding_model():
    
#     embedding = HuggingFaceEmbeddings(
#         model_name = "sentence-transformers/all-MiniLM-L6-v2"
#     )

#     return embedding

import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import GOOGLE_API_KEY

logger = logging.getLogger(__name__)

# Singleton — avoid recreating the model on every request
_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is not None:
        return _embedding_model

    logger.info("Initializing Gemini embedding model (text-embedding-004)...")

    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY is not set. "
            "Please set it in your .env file."
        )

    try:
        _embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY,
            output_dimensionality=768
        )

        # Self-test: generate one embedding to verify it works
        test_vector = _embedding_model.embed_query("initialization test")
        logger.info(
            f"Embedding model ready — dimension: {len(test_vector)}"
        )

    except Exception as e:
        logger.error(f" Failed to initialize embedding model: {e}")
        raise

    return _embedding_model