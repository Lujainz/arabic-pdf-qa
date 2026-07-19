from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    anthropic_api_key: str
    api_key: str
    allowed_origin: str = "http://localhost:3000"
    chroma_db_path: str = "./chroma_db"
    max_file_size_mb: int = 20
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_results: int = 3
    similarity_threshold: float = 0.25  # lowered from 0.5 — better for noisy PDFs

    class Config:
        env_file = ".env"


settings = Settings()