import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.upload import router as upload_router
from routers.query import router as query_router
from core.config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(
    title="Arabic PDF Q&A",
    description="RAG system for Arabic PDF documents.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")
app.include_router(query_router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}