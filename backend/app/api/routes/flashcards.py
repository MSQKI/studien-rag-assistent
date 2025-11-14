"""
Flashcard API Routes
Endpoints for flashcard management and spaced repetition.
"""

from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from loguru import logger

from app.config import get_settings, Settings
from app.api.dependencies import get_flashcard_manager
from app.services.flashcards.flashcard_manager import FlashcardManager

router = APIRouter()


# Request/Response Models
class FlashcardBase(BaseModel):
    subject: str
    question: str
    answer: str
    difficulty: int = 1  # 1-5 scale
    tags: List[str] = []


class FlashcardCreate(FlashcardBase):
    pass


class FlashcardUpdate(BaseModel):
    question: str | None = None
    answer: str | None = None
    difficulty: int | None = None
    tags: List[str] | None = None


class Flashcard(FlashcardBase):
    id: str
    created_at: datetime
    last_reviewed: datetime | None = None
    correct_count: int = 0
    incorrect_count: int = 0
    next_review: datetime | None = None


class AnswerRequest(BaseModel):
    flashcard_id: str
    correct: bool
    time_spent_seconds: int | None = None


class GenerateRequest(BaseModel):
    document_id: str
    subject: str
    count: int = 10


@router.get("", response_model=List[Flashcard])
async def list_flashcards(
    subject: str | None = Query(None, description="Filter by subject"),
    tag: str | None = Query(None, description="Filter by tag"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    manager: FlashcardManager = Depends(get_flashcard_manager)
):
    """
    List all flashcards with optional filters.

    Args:
        subject: Optional subject filter
        tag: Optional tag filter
        limit: Maximum number to return
        offset: Number to skip
        manager: Flashcard manager

    Returns:
        List of flashcards
    """
    try:
        cards = manager.list_flashcards(subject=subject, tag=tag, limit=limit, offset=offset)
        return [Flashcard(**card) for card in cards]
    except Exception as e:
        logger.error(f"Error listing flashcards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("", response_model=Flashcard)
async def create_flashcard(
    flashcard: FlashcardCreate,
    manager: FlashcardManager = Depends(get_flashcard_manager)
):
    """
    Create a new flashcard.

    Args:
        flashcard: Flashcard data
        manager: Flashcard manager

    Returns:
        Created flashcard
    """
    try:
        card_id = manager.create_flashcard(
            subject=flashcard.subject,
            question=flashcard.question,
            answer=flashcard.answer,
            difficulty=flashcard.difficulty,
            tags=flashcard.tags
        )
        card = manager.get_flashcard(card_id)
        return Flashcard(**card)
    except Exception as e:
        logger.error(f"Error creating flashcard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{flashcard_id}", response_model=Flashcard)
async def get_flashcard(
    flashcard_id: str,
    manager: FlashcardManager = Depends(get_flashcard_manager)
):
    """
    Get a specific flashcard.

    Args:
        flashcard_id: Flashcard ID
        manager: Flashcard manager

    Returns:
        Flashcard details
    """
    try:
        card = manager.get_flashcard(flashcard_id)
        if not card:
            raise HTTPException(
                status_code=404,
                detail=f"Flashcard '{flashcard_id}' not found"
            )
        return Flashcard(**card)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting flashcard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{flashcard_id}", response_model=Flashcard)
async def update_flashcard(
    flashcard_id: str,
    update: FlashcardUpdate,
    manager: FlashcardManager = Depends(get_flashcard_manager)
):
    """
    Update a flashcard.

    Args:
        flashcard_id: Flashcard ID
        update: Update data
        manager: Flashcard manager

    Returns:
        Updated flashcard
    """
    try:
        updated = manager.update_flashcard(
            flashcard_id=flashcard_id,
            question=update.question,
            answer=update.answer,
            difficulty=update.difficulty,
            tags=update.tags
        )
        if not updated:
            raise HTTPException(
                status_code=404,
                detail=f"Flashcard '{flashcard_id}' not found"
            )
        return Flashcard(**updated)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating flashcard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear-all")
async def clear_all_flashcards(
    manager: FlashcardManager = Depends(get_flashcard_manager)
):
    """
    Delete ALL flashcards from the database.

    ⚠️ WARNING: This action cannot be undone!

    Args:
        manager: Flashcard manager

    Returns:
        Confirmation message with number of deleted flashcards
    """
    try:
        count = manager.delete_all_flashcards()
        logger.warning(f"Deleted all flashcards: {count} cards removed")
        return {
            "message": f"Successfully deleted all flashcards",
            "deleted_count": count
        }
    except Exception as e:
        logger.error(f"Error deleting all flashcards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{flashcard_id}")
async def delete_flashcard(
    flashcard_id: str,
    manager: FlashcardManager = Depends(get_flashcard_manager)
):
    """
    Delete a flashcard.

    Args:
        flashcard_id: Flashcard ID
        manager: Flashcard manager

    Returns:
        Confirmation message
    """
    try:
        deleted = manager.delete_flashcard(flashcard_id)
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail=f"Flashcard '{flashcard_id}' not found"
            )
        return {"message": f"Flashcard '{flashcard_id}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting flashcard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/next/due", response_model=Flashcard | None)
async def get_next_flashcard(
    subject: str | None = Query(None, description="Filter by subject"),
    manager: FlashcardManager = Depends(get_flashcard_manager)
):
    """
    Get the next flashcard due for review (spaced repetition).

    Args:
        subject: Optional subject filter
        manager: Flashcard manager

    Returns:
        Next flashcard to review or None if no cards are due
    """
    try:
        card = manager.get_next_due_flashcard(subject=subject)
        if not card:
            return None  # Return None instead of 404 for better UX
        return Flashcard(**card)
    except Exception as e:
        logger.error(f"Error getting next flashcard: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/answer")
async def record_answer(
    answer: AnswerRequest,
    manager: FlashcardManager = Depends(get_flashcard_manager)
):
    """
    Record an answer and update spaced repetition schedule.

    Args:
        answer: Answer data
        manager: Flashcard manager

    Returns:
        Updated flashcard and next review date
    """
    try:
        updated = manager.record_answer(
            flashcard_id=answer.flashcard_id,
            correct=answer.correct,
            time_spent_seconds=answer.time_spent_seconds
        )
        return {
            "flashcard": Flashcard(**updated),
            "next_review": updated.get("next_review"),
            "message": "Answer recorded successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error recording answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate", response_model=List[Flashcard])
async def generate_flashcards(
    request: GenerateRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Auto-generate flashcards from a document.

    Args:
        request: Generation request with document ID
        settings: Application settings

    Returns:
        List of generated flashcards
    """
    # TODO: Implement automatic flashcard generation
    raise HTTPException(
        status_code=501,
        detail="Flashcard generation not yet implemented"
    )


@router.get("/stats/overview")
async def get_study_stats(
    manager: FlashcardManager = Depends(get_flashcard_manager)
):
    """
    Get study statistics overview.

    Args:
        manager: Flashcard manager

    Returns:
        Study statistics
    """
    try:
        stats = manager.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
