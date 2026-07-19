import logging
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from core.config import settings
from core.models import QueryResponse, SourceChunk, UsageInfo
from services.retriever import retrieve_relevant_chunks
from services.prompt_builder import build_prompt
from services.generator import generate_answer, NO_CONTEXT_MESSAGE

logger = logging.getLogger(__name__)
router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    collection_id: str      # returned by /upload — no need to remember the filename


@router.post("/query", response_model=QueryResponse)
async def query_pdf(
    request: QueryRequest,
    x_api_key: str = Header(...),
):
    # Auth check
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    if not request.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty.")

    # Step 1: Retrieve relevant chunks
    chunks = retrieve_relevant_chunks(request.question, request.collection_id)
    logger.info(f"Retrieved {len(chunks)} relevant chunks above similarity threshold.")

    # Step 2: Graceful fallback if nothing relevant found
    if not chunks:
        return QueryResponse(
            answer=NO_CONTEXT_MESSAGE,
            sources=[],
            usage=None,
        )

    # Step 3: Build the Arabic prompt
    prompt = build_prompt(request.question, chunks)

    # Step 4: Call Claude
    result = generate_answer(prompt)

    # Step 5: Return answer + sources + token usage
    return QueryResponse(
        answer=result["answer"],
        sources=[
            SourceChunk(
                filename=chunk["filename"],
                page=chunk["page_number"],
                similarity=chunk["similarity"],
                chunk_text=chunk["text"][:200],
            )
            for chunk in chunks
        ],
        usage=UsageInfo(
            input_tokens=result["input_tokens"],
            output_tokens=result["output_tokens"],
            estimated_cost_usd=result["estimated_cost_usd"],
        ),
    )