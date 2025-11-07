"""
Shared dependencies for API routes.
"""

from typing import Optional
from functools import lru_cache

from app.config import get_settings, Settings
from app.services.rag.rag_chain import RAGAssistant
from app.services.flashcards.flashcard_manager import FlashcardManager, get_flashcard_manager
from app.services.graph.graph_builder import GraphBuilder, get_graph_builder
from app.services.graph.entity_extractor import EntityExtractor
from app.services.voice.session_manager import SessionManager, get_session_manager


# Singleton instances
_rag_assistant: Optional[RAGAssistant] = None
_entity_extractor: Optional[EntityExtractor] = None


def get_rag_assistant() -> RAGAssistant:
    """
    Get or create RAG assistant instance.

    Returns:
        RAGAssistant instance
    """
    global _rag_assistant
    if _rag_assistant is None:
        _rag_assistant = RAGAssistant()
    return _rag_assistant


def get_entity_extractor() -> EntityExtractor:
    """
    Get or create entity extractor instance.

    Returns:
        EntityExtractor instance
    """
    global _entity_extractor
    if _entity_extractor is None:
        _entity_extractor = EntityExtractor()
    return _entity_extractor


# Re-export for convenience
__all__ = [
    'get_settings',
    'get_rag_assistant',
    'get_flashcard_manager',
    'get_graph_builder',
    'get_entity_extractor',
    'get_session_manager'
]
