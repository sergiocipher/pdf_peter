"""
Debug Pipeline
--------------
Tests each component of the RAG pipeline in isolation to identify failures.

Usage:
    python debug_pipeline.py
"""

from dotenv import load_dotenv
import os
import sys

load_dotenv()


def check_env_vars():
    """Step 1: Verify all environment variables are loaded."""
    print("=" * 60)
    print("STEP 1: Checking environment variables")
    print("=" * 60)

    required_vars = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "QDRANT_URL": os.getenv("QDRANT_URL"),
        "QDRANT_API_KEY": os.getenv("QDRANT_API_KEY"),
    }

    all_ok = True
    for name, value in required_vars.items():
        if value:
            # Show first 10 chars only for security
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {name} = {masked}")
        else:
            print(f"  ❌ {name} is NOT SET")
            all_ok = False

    return all_ok


def check_embeddings():
    """Step 2: Verify Gemini embeddings work and check dimensions."""
    print("\n" + "=" * 60)
    print("STEP 2: Testing Gemini embeddings")
    print("=" * 60)

    try:
        from app.services.embeddings import get_embedding_model

        embedding_model = get_embedding_model()
        print("  ✅ Embedding model instantiated")

        # Generate a test embedding
        test_text = "This is a test sentence for embedding."
        vector = embedding_model.embed_query(test_text)

        print(f"  ✅ Test embedding generated successfully")
        print(f"  📏 Embedding dimension: {len(vector)}")
        print(f"  📊 First 5 values: {vector[:5]}")

        if len(vector) == 768:
            print(f"  ✅ Dimension is 768 (gemini-embedding-001 with MRL truncation)")
        else:
            print(f"  ⚠️  Unexpected dimension: {len(vector)} (expected 768)")

        return True, len(vector)

    except Exception as e:
        print(f"  ❌ Embedding failed: {type(e).__name__}: {e}")
        return False, None


def check_qdrant_connection():
    """Step 3: Verify Qdrant connection and collection config."""
    print("\n" + "=" * 60)
    print("STEP 3: Testing Qdrant connection")
    print("=" * 60)

    try:
        from qdrant_client import QdrantClient

        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        print(f"  ✅ Connected to Qdrant at {qdrant_url}")

        # List collections
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]
        print(f"  📋 Collections: {collection_names}")

        # Check our specific collection
        if "rag-notebooklm" in collection_names:
            info = client.get_collection("rag-notebooklm")
            vectors_config = info.config.params.vectors
            print(f"\n  Collection 'rag-notebooklm':")
            print(f"    Vector size: {vectors_config.size}")
            print(f"    Distance:    {vectors_config.distance}")
            print(f"    Points:      {info.points_count}")

            if vectors_config.size == 768:
                print(f"    ✅ Vector size matches Gemini embeddings (768)")
            elif vectors_config.size == 384:
                print(f"    ❌ Vector size is 384 (HuggingFace) — NEEDS RESET!")
                print(f"    👉 Run: python reset_qdrant.py")
                return False
            else:
                print(f"    ⚠️  Unexpected vector size: {vectors_config.size}")
        else:
            print(f"\n  ⚠️  Collection 'rag-notebooklm' does not exist yet.")
            print(f"     It will be created on first PDF upload.")

        return True

    except Exception as e:
        print(f"  ❌ Qdrant connection failed: {type(e).__name__}: {e}")
        return False


def check_retrieval():
    """Step 4: Test a similarity search (only if collection exists with data)."""
    print("\n" + "=" * 60)
    print("STEP 4: Testing retrieval")
    print("=" * 60)

    try:
        from qdrant_client import QdrantClient

        client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

        # Check if collection exists and has data
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]

        if "rag-notebooklm" not in collection_names:
            print("  ⏭️  Skipped — collection doesn't exist yet. Upload a PDF first.")
            return True

        info = client.get_collection("rag-notebooklm")
        if info.points_count == 0:
            print("  ⏭️  Skipped — collection is empty. Upload a PDF first.")
            return True

        # Try actual retrieval via LangChain
        from app.services.embeddings import get_embedding_model
        from app.services.retriever import retrieve_chunks

        embedding_model = get_embedding_model()
        results = retrieve_chunks(
            query="What is this document about?",
            embedding_model=embedding_model,
            k=3
        )

        print(f"  ✅ Retrieved {len(results)} chunks")
        for i, doc in enumerate(results):
            page = doc.metadata.get("page", "?")
            preview = doc.page_content[:80].replace("\n", " ")
            print(f"    [{i+1}] Page {page}: {preview}...")

        return True

    except Exception as e:
        print(f"  ❌ Retrieval failed: {type(e).__name__}: {e}")
        return False


def check_groq_llm():
    """Step 5: Test the Groq LLM connection."""
    print("\n" + "=" * 60)
    print("STEP 5: Testing Groq LLM")
    print("=" * 60)

    try:
        from groq import Groq

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Say 'hello' and nothing else."}
            ],
            max_tokens=10,
        )

        answer = response.choices[0].message.content
        print(f"  ✅ Groq LLM responded: {answer}")
        return True

    except Exception as e:
        print(f"  ❌ Groq LLM failed: {type(e).__name__}: {e}")
        return False


def main():
    print("🔍 RAG NotebookLM — Pipeline Debug Tool")
    print("=" * 60)

    results = {}

    results["env"] = check_env_vars()
    results["embeddings"] = check_embeddings()[0]
    results["qdrant"] = check_qdrant_connection()
    results["retrieval"] = check_retrieval()
    results["groq"] = check_groq_llm()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\n🎉 All checks passed! Your pipeline is ready.")
    else:
        print("\n⚠️  Some checks failed. Fix the issues above and re-run.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
