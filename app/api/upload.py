from fastapi import APIRouter , UploadFile , File , HTTPException
import os 
import shutil

from app.services.pdf_loader import load_pdf

from app.services.chunking import chunk_documents

from app.services.embeddings import get_embedding_model

from app.services.vector_store import store_documents

router = APIRouter()

Upload_DIR = "uploads"

@router.post("/uploads")
async def upload_pdf(file: UploadFile = File(...)):

    #validate pdf 
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="only pdf files are allowed !!!"
        )
    
    #create uploads folder if not exits 
    os.makedirs(Upload_DIR , exist_ok=True)

    #save file path 
    file_path = os.path.join(Upload_DIR , file.filename)

    #save file
    with open(file_path , "wb") as buffer:
        shutil.copyfileobj(file.file , buffer)
    
    #load pdf 
    documents = load_pdf(file_path)

    #chunk document 
    chunks = chunk_documents(documents)

    #embedding 
    embedding_model = get_embedding_model()

    #test embedding 
    sample_vector = embedding_model.embed_query(
        chunks[0].page_content
    )

    #store in qdrant 
    store_documents(chunks=chunks, embedding_model=embedding_model)


    return{
        "message":"PDF uploaded and parsed succesfully !!",
        "total_pages": len(documents),
        "total_chunks": len(chunks),
        "embedding_dimension": len(sample_vector)
    }

# sudo docker run -p 6333:6333 qdrant/qdrant