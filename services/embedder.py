from openai import OpenAI
from core.config import settings


client = OpenAI(api_key=settings.openai_api_key)

EMBEDDING_MODEL = "text-embedding-3-large"


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Takes a list of chunk dicts.
    Returns the same list with an added 'embedding' field on each chunk.
    Calls OpenAI in a single batch request for efficiency.
    """
    texts = [chunk["text"] for chunk in chunks]

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )

    for i, chunk in enumerate(chunks):
        chunk["embedding"] = response.data[i].embedding

    return chunks


def embed_query(query: str) -> list[float]:
    """
    Embeds a single query string using the same model as the chunks.
    Must use the same model — different models produce incompatible vector spaces.
    """
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=[query],
    )
    return response.data[0].embedding