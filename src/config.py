"""
Configuration module for the RAG Assistant.
Uses Pydantic Settings for type-safe configuration management.
"""

from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key for embeddings and LLM")

    # Model Configuration
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model to use"
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        description="OpenAI LLM model for chat completions"
    )
    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        description="LLM temperature for response generation"
    )
    max_tokens: int = Field(
        default=2000,
        gt=0,
        description="Maximum tokens for LLM responses"
    )

    # Document Processing Configuration
    chunk_size: int = Field(
        default=1000,
        gt=0,
        description="Size of text chunks for document splitting"
    )
    chunk_overlap: int = Field(
        default=200,
        ge=0,
        description="Overlap between consecutive chunks"
    )

    # Storage Paths
    chroma_persist_dir: Path = Field(
        default=Path("./data/chroma_db"),
        description="Directory for persistent ChromaDB storage"
    )
    upload_dir: Path = Field(
        default=Path("./data/uploads"),
        description="Directory for uploaded PDF files"
    )

    # Vector Store Configuration
    collection_name: str = Field(
        default="study_documents",
        description="ChromaDB collection name"
    )
    retrieval_k: int = Field(
        default=4,
        gt=0,
        description="Number of documents to retrieve for RAG"
    )

    # Application Settings
    app_name: str = Field(
        default="Studien-RAG-Assistent",
        description="Application name"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )

    # Performance Settings
    batch_size: int = Field(
        default=10,
        gt=0,
        description="Batch size for document processing"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @field_validator("chunk_overlap")
    @classmethod
    def validate_chunk_overlap(cls, v: int, info) -> int:
        """Ensure chunk overlap is less than chunk size."""
        if "chunk_size" in info.data and v >= info.data["chunk_size"]:
            raise ValueError("chunk_overlap must be less than chunk_size")
        return v

    def create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance (singleton pattern).

    Returns:
        Settings: Application settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.create_directories()
    return _settings


def reload_settings() -> Settings:
    """
    Reload settings from environment (useful for testing).

    Returns:
        Settings: Fresh settings instance
    """
    global _settings
    _settings = None
    return get_settings()
