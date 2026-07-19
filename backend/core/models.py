from pydantic import BaseModel


# --- Upload ---

class UploadResponse(BaseModel):
    message: str
    filename: str
    collection_id: str      # sanitized collection name — use this to query later
    pages_extracted: int
    chunks_stored: int


# --- Query ---

class SourceChunk(BaseModel):
    filename: str
    page: int
    similarity: float
    chunk_text: str


class UsageInfo(BaseModel):
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    usage: UsageInfo | None = None  # None when fallback message is returned