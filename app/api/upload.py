import logging
import os
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_loader import load_pdf
from app.services.chunking import chunk_documents
from app.services.embeddings import get_embedding_model
from app.services.vector_store import store_documents

logger = logging.getLogger(__name__)

router = APIRouter()

Upload_DIR = "uploads"



@router.post("/uploads")
def upload_pdf(file: UploadFile = File(...)):

    logger.info(f"📄 Upload started: {file.filename} ({file.content_type})")

    # validate pdf
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="only pdf files are allowed !!!"
        )

    try:
        # create uploads folder if not exists
        os.makedirs(Upload_DIR, exist_ok=True)

        # save file path
        file_path = os.path.join(Upload_DIR, file.filename)

        # save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"  Step 1/4: File saved to {file_path}")

        # load pdf
        documents = load_pdf(file_path)
        logger.info(f"  Step 2/4: Loaded {len(documents)} pages from PDF")

        # chunk document
        chunks = chunk_documents(documents)
        logger.info(f"  Step 3/4: Split into {len(chunks)} chunks")

        # embedding
        embedding_model = get_embedding_model()

        # test embedding
        sample_vector = embedding_model.embed_query(
            chunks[0].page_content
        )
        logger.info(
            f"  Embedding test: dimension={len(sample_vector)}, "
            f"sample values={sample_vector[:3]}"
        )

        # store in qdrant
        store_documents(chunks=chunks, embedding_model=embedding_model)
        logger.info(f"  Step 4/4: Stored in Qdrant ✅")

        return {
            "message": "PDF uploaded and parsed succesfully !!",
            "total_pages": len(documents),
            "total_chunks": len(chunks),
            "embedding_dimension": len(sample_vector)
        }

    except Exception as e:
        logger.error(f"❌ Upload pipeline failed: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Upload processing failed: {str(e)}"
        )

# sudo docker run -p 6333:6333 qdrant/qdrant