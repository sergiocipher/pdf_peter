from fastapi import FastAPI
from app.api.upload import router as upload_router

app = FastAPI(
    title = "RAG notebook clone"
)

@app.get("/")

def health_check():
    return{
        "message":"Server is running!!"
    }

app.include_router(upload_router)