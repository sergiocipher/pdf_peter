"""
Reset Qdrant Collection
-----------------------
Deletes the 'rag-notebooklm' collection so it can be recreated
with the correct vector dimensions for Gemini embeddings (768-dim).

Usage:
    python reset_qdrant.py
"""

from dotenv import load_dotenv
import os
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "rag-notebooklm"


def main():
    print(f"Connecting to Qdrant at: {QDRANT_URL}")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # List existing collections
    collections = client.get_collections().collections
    collection_names = [c.name for c in collections]
    print(f"Existing collections: {collection_names}")

    if COLLECTION_NAME in collection_names:
        # Show current collection info before deleting
        collection_info = client.get_collection(COLLECTION_NAME)
        vectors_config = collection_info.config.params.vectors
        print(f"\nCollection '{COLLECTION_NAME}' found:")
        print(f"  Vector size: {vectors_config.size}")
        print(f"  Distance:    {vectors_config.distance}")
        print(f"  Points:      {collection_info.points_count}")

        # Delete the collection
        client.delete_collection(COLLECTION_NAME)
        print(f"\n✅ Collection '{COLLECTION_NAME}' deleted successfully!")
        print("   You can now re-upload your PDF via /api/uploads")
        print("   The new collection will be created with 768-dim vectors (Gemini)")
    else:
        print(f"\n⚠️  Collection '{COLLECTION_NAME}' does not exist. Nothing to delete.")
        print("   You can proceed to upload your PDF via /api/uploads")


if __name__ == "__main__":
    main()
