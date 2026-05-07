from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.upload import router as upload_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="RAG NotebookLM Clone"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "message": "Server is running"
    }

app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")