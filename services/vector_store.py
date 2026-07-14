import logging
import chromadb
from fastapi import HTTPException
from core.config import settings

logger = logging.getLogger(__name__)
client = chromadb.PersistentClient(path=settings.chroma_db_path)


def get_or_create_collection(collection_name: str):
    """
    Returns an existing ChromaDB collection or creates one if it doesn't exist.
    Each uploaded PDF gets its own collection, named by its filename.
    """
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def store_chunks(chunks: list[dict], filename: str) -> int:
    """
    Stores embedded chunks in ChromaDB.
    Returns the number of chunks stored.
    Raises HTTP 409 if this file has already been uploaded,
    so the user gets a clear message instead of a silent duplicate or ID collision.
    """
    collection_name = sanitize_collection_name(filename)
    collection = get_or_create_collection(collection_name)

    # Duplicate upload check — if chunks already exist, reject cleanly
    existing_count = collection.count()
    if existing_count > 0:
        logger.warning(
            f"Duplicate upload attempt for '{filename}' "
            f"— collection already has {existing_count} chunks."
        )
        raise HTTPException(
            status_code=409,
            detail=f"'{filename}' has already been uploaded and indexed. "
                   "Delete the existing document first if you want to re-upload."
        )

    ids = [f"{collection_name}_chunk_{chunk['chunk_index']}" for chunk in chunks]
    embeddings = [chunk["embedding"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [
        {
            "filename": filename,
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    stored = len(chunks)
    logger.info(f"Stored {stored} chunks for '{filename}'.")
    return stored


def query_collection(collection_name: str, query_embedding: list[float], top_k: int) -> list[dict]:
    """
    Searches a ChromaDB collection for the top-k most similar chunks.
    Returns a list of results with text, metadata, and similarity distance.
    """
    collection = get_or_create_collection(collection_name)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for i in range(len(results["ids"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return chunks


def sanitize_collection_name(filename: str) -> str:
    """
    ChromaDB collection names must be alphanumeric + hyphens, 3-63 chars.
    Strip the extension and replace unsafe characters.
    """
    name = filename.rsplit(".", 1)[0]
    sanitized = "".join(c if c.isalnum() or c == "-" else "-" for c in name)
    sanitized = sanitized.strip("-")[:63]
    if len(sanitized) < 3:
        sanitized = sanitized + "-doc"
    return sanitized.lower()