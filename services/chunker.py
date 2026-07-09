from langchain_text_splitters import RecursiveCharacterTextSplitter
from core.config import settings


def chunk_pages(pages: list[dict]) -> list[dict]:
    """
    Takes a list of {page_number, text} dicts.
    Returns a list of chunks with metadata: text, page_number, chunk_index.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    chunks = []
    chunk_index = 0

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for chunk_text in page_chunks:
            if not chunk_text.strip():
                continue

            chunks.append({
                "text": chunk_text.strip(),
                "page_number": page["page_number"],
                "chunk_index": chunk_index,
            })
            chunk_index += 1

    return chunks