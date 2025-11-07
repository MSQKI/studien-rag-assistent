"""
RAG API Routes
Endpoints for document-based question answering.
"""

from typing import List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from loguru import logger

from app.api.dependencies import get_rag_assistant, get_settings
from app.services.rag.rag_chain import RAGAssistant
from app.config import Settings

router = APIRouter()


# Request/Response Models
class QueryRequest(BaseModel):
    question: str
    conversation_id: str | None = None


class Source(BaseModel):
    file: str
    page: int
    content_preview: str


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    conversation_id: str


class ConversationClearResponse(BaseModel):
    message: str
    conversation_id: str | None = None


class StatsResponse(BaseModel):
    total_documents: int
    total_chunks: int
    conversation_length: int
    model: str


@router.post("/query", response_model=QueryResponse)
async def query_documents(
    request: QueryRequest,
    assistant: RAGAssistant = Depends(get_rag_assistant)
):
    """
    Query the knowledge base with RAG.

    Args:
        request: Query request with question
        assistant: RAG assistant instance

    Returns:
        Answer with sources and citations
    """
    try:
        # Query the RAG system
        result = assistant.ask(request.question)

        # Convert sources to response model
        sources = [
            Source(
                file=src["file"],
                page=src["page"],
                content_preview=src["content_preview"]
            )
            for src in result["sources"]
        ]

        return QueryResponse(
            answer=result["answer"],
            sources=sources,
            conversation_id=request.conversation_id or "default"
        )

    except Exception as e:
        logger.error(f"Error in RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear", response_model=ConversationClearResponse)
async def clear_conversation(
    conversation_id: str | None = None,
    assistant: RAGAssistant = Depends(get_rag_assistant)
):
    """
    Clear conversation history.

    Args:
        conversation_id: Optional conversation ID
        assistant: RAG assistant instance

    Returns:
        Confirmation message
    """
    try:
        assistant.clear_conversation()
        logger.info("Cleared conversation history")

        return ConversationClearResponse(
            message="Conversation cleared successfully",
            conversation_id=conversation_id
        )

    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    assistant: RAGAssistant = Depends(get_rag_assistant)
):
    """
    Get RAG system statistics.

    Args:
        assistant: RAG assistant instance

    Returns:
        System statistics
    """
    try:
        stats = assistant.get_stats()

        return StatsResponse(
            total_documents=len(assistant.get_all_documents()),
            total_chunks=stats["collection"]["document_count"],
            conversation_length=stats["conversation_length"],
            model=stats["model"]
        )

    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
