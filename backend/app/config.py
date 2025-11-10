"""
Configuration module for the Study Platform.
Extends the existing RAG configuration with Voice, Graph, and Flashcard settings.
"""

from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application Settings
    app_name: str = Field(
        default="Study Platform",
        description="Application name"
    )
    app_version: str = Field(
        default="2.0.0",
        description="Application version"
    )
    debug: bool = Field(
        default=False,
        description="Debug mode"
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )

    # API Configuration
    api_prefix: str = Field(
        default="/api",
        description="API prefix for all routes"
    )
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8501"],
        description="Allowed CORS origins"
    )

    # OpenAI Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")

    # Model Configuration - RAG
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="OpenAI embedding model"
    )
    llm_model: str = Field(
        default="gpt-4o-mini",
        description="OpenAI LLM model for chat"
    )
    temperature: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        description="LLM temperature"
    )
    max_tokens: int = Field(
        default=2000,
        gt=0,
        description="Maximum tokens for LLM"
    )

    # Document Processing
    chunk_size: int = Field(
        default=1000,
        gt=0,
        description="Text chunk size"
    )
    chunk_overlap: int = Field(
        default=200,
        ge=0,
        description="Chunk overlap"
    )

    # Advanced PDF Processing (State-of-the-art 2025)
    use_advanced_pdf_processing: bool = Field(
        default=True,
        description="Use Unstructured.io for tables/images (requires additional dependencies)"
    )
    use_vision_for_images: bool = Field(
        default=False,
        description="Use GPT-4 Vision for image/table descriptions (slower, costs more)"
    )

    # Storage Paths
    data_dir: Path = Field(
        default=Path("./data"),
        description="Base data directory"
    )
    chroma_persist_dir: Path = Field(
        default=Path("./data/chroma_db"),
        description="ChromaDB storage"
    )
    upload_dir: Path = Field(
        default=Path("./data/uploads"),
        description="PDF uploads directory"
    )
    flashcards_db_path: Path = Field(
        default=Path("./data/flashcards/flashcards.db"),
        description="SQLite flashcards database"
    )

    # Vector Store Configuration
    collection_name: str = Field(
        default="study_documents",
        description="ChromaDB collection name"
    )
    retrieval_k: int = Field(
        default=4,
        gt=0,
        description="Number of documents to retrieve"
    )

    # Neo4j Configuration
    neo4j_uri: str = Field(
        default="bolt://localhost:7687",
        description="Neo4j connection URI"
    )
    neo4j_user: str = Field(
        default="neo4j",
        description="Neo4j username"
    )
    neo4j_password: str = Field(
        default="password123",
        description="Neo4j password"
    )
    neo4j_database: str = Field(
        default="neo4j",
        description="Neo4j database name"
    )

    # Voice Buddy Configuration
    realtime_model: str = Field(
        default="gpt-4o-realtime-preview",
        description="OpenAI Realtime model"
    )
    voice_name: str = Field(
        default="alloy",
        description="Voice name for TTS"
    )
    audio_format: str = Field(
        default="pcm16",
        description="Audio format"
    )
    sample_rate: int = Field(
        default=24000,
        description="Audio sample rate"
    )
    turn_detection_type: str = Field(
        default="server_vad",
        description="Turn detection type"
    )
    vad_threshold: float = Field(
        default=0.5,
        description="VAD threshold"
    )
    vad_silence_duration_ms: int = Field(
        default=500,
        description="VAD silence duration"
    )

    # Flashcard Configuration
    flashcard_generation_enabled: bool = Field(
        default=True,
        description="Enable automatic flashcard generation"
    )
    flashcards_per_document: int = Field(
        default=15,
        description="Max flashcards to generate per document on initial upload"
    )
    flashcards_max_per_generation: int = Field(
        default=20,
        description="Max flashcards to generate when manually requesting more"
    )
    spaced_repetition_algorithm: str = Field(
        default="sm2",
        description="Spaced repetition algorithm (sm2, anki)"
    )

    # Graph Configuration
    entity_extraction_enabled: bool = Field(
        default=True,
        description="Enable entity extraction for graph"
    )
    entity_confidence_threshold: float = Field(
        default=0.7,
        description="Minimum confidence for entity extraction"
    )
    graph_visualization_enabled: bool = Field(
        default=True,
        description="Enable graph visualization"
    )

    # Performance Settings
    batch_size: int = Field(
        default=10,
        gt=0,
        description="Batch size for processing"
    )
    max_upload_size_mb: int = Field(
        default=50,
        description="Maximum file upload size in MB"
    )

    # Session Settings
    session_timeout_minutes: int = Field(
        default=15,
        description="Session timeout in minutes"
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
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_persist_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        # Create flashcards directory
        self.flashcards_db_path.parent.mkdir(parents=True, exist_ok=True)


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
    Reload settings from environment.

    Returns:
        Settings: Fresh settings instance
    """
    global _settings
    _settings = None
    return get_settings()
