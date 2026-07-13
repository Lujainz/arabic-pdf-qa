import logging
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from core.config import settings
from services.retriever import retrieve_relevant_chunks
from services.prompt_builder import build_prompt
from services.generator import generate_answer, NO_CONTEXT_MESSAGE
from services.vector_store import sanitize_collection_name

logger = logging.getLogger(__name__)
router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    filename: str  # the originally uploaded PDF filename, used to find its collection


@router.post("/query")
async def query_pdf(
    request: QueryRequest,
    x_api_key: str = Header(...),
):
    # Auth check
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    if not request.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty.")

    collection_name = sanitize_collection_name(request.filename)

    # Step 1: Retrieve relevant chunks
    chunks = retrieve_relevant_chunks(request.question, collection_name)
    logger.info(f"Retrieved {len(chunks)} relevant chunks above similarity threshold.")

    # Step 2: Graceful fallback if nothing relevant found
    if not chunks:
        return {
            "answer": NO_CONTEXT_MESSAGE,
            "sources": [],
        }

    # Step 3: Build the Arabic prompt
    prompt = build_prompt(request.question, chunks)

    # Step 4: Call Claude
    result = generate_answer(prompt)

    # Step 5: Return answer + sources + token usage
    return {
        "answer": result["answer"],
        "sources": [
            {
                "filename": chunk["filename"],
                "page": chunk["page_number"],
                "similarity": chunk["similarity"],
                "chunk_text": chunk["text"][:200],  # preview only
            }
            for chunk in chunks
        ],
        "usage": {
            "input_tokens": result["input_tokens"],
            "output_tokens": result["output_tokens"],
            "estimated_cost_usd": result["estimated_cost_usd"],
        },
    }