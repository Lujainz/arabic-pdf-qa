import chromadb
from core.config import settings


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
    Each chunk gets a unique ID, its embedding, text, and metadata.
    """
    collection_name = sanitize_collection_name(filename)
    collection = get_or_create_collection(collection_name)

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

    return len(chunks)


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
    ChromaDB collection names must be alphanumeric + hyphens, 3–63 chars.
    Strip the extension and replace unsafe characters.
    """
    name = filename.rsplit(".", 1)[0]
    sanitized = "".join(c if c.isalnum() or c == "-" else "-" for c in name)
    sanitized = sanitized.strip("-")[:63]
    if len(sanitized) < 3:
        sanitized = sanitized + "-doc"
    return sanitized.lower()