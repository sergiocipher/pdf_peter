from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="RAG NotebookLM Clone"
)

@app.get("/")
def health_check():
    return {
        "message": "Server is running"
    }

app.include_router(upload_router)
app.include_router(chat_router)