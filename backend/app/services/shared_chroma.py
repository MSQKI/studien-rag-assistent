"""
Shared ChromaDB Client
Provides a singleton ChromaDB client to avoid multiple instances with different settings.
"""

from typing import Optional
import chromadb
from chromadb.api import ClientAPI
from chromadb.config import Settings as ChromaSettings
from loguru import logger

from app.config import get_settings


_chroma_client: Optional[ClientAPI] = None


def get_chroma_client() -> ClientAPI:
    """
    Get or create a shared ChromaDB client instance.

    Returns:
        ChromaDB client instance
    """
    global _chroma_client

    if _chroma_client is None:
        settings = get_settings()
        _chroma_client = chromadb.PersistentClient(
            path=str(settings.chroma_persist_dir),
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        logger.info(f"Created shared ChromaDB client at {settings.chroma_persist_dir}")

    return _chroma_client


def reset_chroma_client() -> None:
    """Reset the shared ChromaDB client (useful for testing)."""
    global _chroma_client
    _chroma_client = None
    logger.info("Reset shared ChromaDB client")
