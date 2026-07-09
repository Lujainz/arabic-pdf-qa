import logging
from fastapi import APIRouter, UploadFile, File, Header, HTTPException

from core.config import settings
from services.pdf_extractor import extract_text_from_pdf
from services.chunker import chunk_pages
from services.embedder import embed_chunks
from services.vector_store import store_chunks

logger = logging.getLogger(__name__)
router = APIRouter()

MAX_FILE_SIZE_BYTES = settings.max_file_size_mb * 1024 * 1024


@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    x_api_key: str = Header(...),
):
    # Auth check
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    # File type check
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=422, detail="Only PDF files are accepted.")

    # Read and size check
    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=422,
            detail=f"File too large. Maximum allowed size is {settings.max_file_size_mb}MB."
        )

    logger.info(f"Processing upload: {file.filename} ({len(file_bytes) / 1024:.1f} KB)")

    # Step 1: Extract Arabic text
    pages = extract_text_from_pdf(file_bytes, file.filename)
    logger.info(f"Extracted text from {len(pages)} pages.")

    # Step 2: Chunk the text
    chunks = chunk_pages(pages)
    if not chunks:
        raise HTTPException(status_code=422, detail="No text chunks could be created from this PDF.")
    logger.info(f"Created {len(chunks)} chunks.")

    # Step 3: Embed chunks
    chunks = embed_chunks(chunks)
    logger.info(f"Embedded {len(chunks)} chunks.")

    # Step 4: Store in ChromaDB
    stored_count = store_chunks(chunks, file.filename)
    logger.info(f"Stored {stored_count} chunks in ChromaDB for '{file.filename}'.")

    return {
        "message": "PDF processed successfully.",
        "filename": file.filename,
        "pages_extracted": len(pages),
        "chunks_stored": stored_count,
    }