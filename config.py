"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4o-mini"
    
    # ChromaDB
    chroma_persist_dir: str = "./chroma_data"
    chroma_collection_name: str = "knowledge_base"
    
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # Processing
    max_chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    
    # Scraping
    scrape_timeout: int = 30
    max_concurrent_scrapes: int = 3
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
