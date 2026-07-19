import logging
from openai import OpenAI, OpenAIError
from fastapi import HTTPException
from core.config import settings

logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.openai_api_key)

EMBEDDING_MODEL = "text-embedding-3-large"


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Takes a list of chunk dicts.
    Returns the same list with an added 'embedding' field on each chunk.
    Calls OpenAI in a single batch request for efficiency.
    Raises HTTP 503 if OpenAI is unavailable or returns an error.
    """
    texts = [chunk["text"] for chunk in chunks]

    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts,
        )
    except OpenAIError as e:
        logger.error(f"OpenAI embedding error: {e}")
        raise HTTPException(
            status_code=503,
            detail="Embedding service unavailable — please try again shortly."
        )

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = response.data[i].embedding

    return chunks


def embed_query(query: str) -> list[float]:
    """
    Embeds a single query string using the same model as the chunks.
    Must use the same model — different models produce incompatible vector spaces.
    Raises HTTP 503 if OpenAI is unavailable or returns an error.
    """
    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=[query],
        )
    except OpenAIError as e:
        logger.error(f"OpenAI embedding error: {e}")
        raise HTTPException(
            status_code=503,
            detail="Embedding service unavailable — please try again shortly."
        )

    return response.data[0].embedding