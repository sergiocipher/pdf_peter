from fastapi import APIRouter , UploadFile , File , HTTPException
import os 
import shutil

from app.services.pdf_loader import load_pdf

from app.services.chunking import chunk_documents

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


    return{
        "message":"PDF uploaded and parsed succesfully !!",
        "total_pages": len(documents),
        "total_chunks": len(chunks),
        "sample_chunk": chunks[0].page_content
    }