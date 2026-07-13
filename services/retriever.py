from services.embedder import embed_query
from services.vector_store import query_collection
from core.config import settings


def retrieve_relevant_chunks(question: str, collection_name: str) -> list[dict]:
    """
    Embeds the user's question and retrieves the top-k most similar chunks
    from the given ChromaDB collection.

    ChromaDB returns 'distance' (lower = more similar) when using cosine space.
    We convert distance to a similarity score (higher = more similar) and
    filter out chunks below the configured threshold.
    """
    query_embedding = embed_query(question)

    raw_results = query_collection(
        collection_name=collection_name,
        query_embedding=query_embedding,
        top_k=settings.top_k_results,
    )

    relevant_chunks = []
    for result in raw_results:
        similarity = 1 - result["distance"]  # cosine distance -> similarity
        if similarity >= settings.similarity_threshold:
            relevant_chunks.append({
                "text": result["text"],
                "filename": result["metadata"]["filename"],
                "page_number": result["metadata"]["page_number"],
                "similarity": round(similarity, 3),
            })

    return relevant_chunks