"""
Progress Streaming API Routes
Server-Sent Events (SSE) for real-time progress updates.
"""

import json
import asyncio
from typing import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from loguru import logger

from app.services.progress_tracker import get_progress_tracker

router = APIRouter()


async def event_generator(document_id: str) -> AsyncGenerator[str, None]:
    """
    Generate SSE events for document processing progress.

    Args:
        document_id: Document ID to track

    Yields:
        SSE formatted event strings
    """
    tracker = get_progress_tracker()
    queue = await tracker.subscribe(document_id)

    try:
        logger.info(f"SSE connection established for document {document_id}")

        while True:
            # Wait for progress update with timeout
            try:
                progress_data = await asyncio.wait_for(queue.get(), timeout=30.0)

                # Format as SSE event
                event_data = json.dumps(progress_data)
                yield f"data: {event_data}\n\n"

                # If completed or error, send final event and close
                status = progress_data.get("status")
                if status in ["completed", "error"]:
                    logger.info(f"Document {document_id} processing {status}, closing SSE")
                    break

            except asyncio.TimeoutError:
                # Send keepalive ping every 30s
                yield f": keepalive\n\n"

    except asyncio.CancelledError:
        logger.info(f"SSE connection cancelled for document {document_id}")
    except Exception as e:
        logger.error(f"Error in SSE stream for {document_id}: {str(e)}")
        error_event = json.dumps({
            "status": "error",
            "error": str(e)
        })
        yield f"data: {error_event}\n\n"
    finally:
        tracker.unsubscribe(document_id, queue)
        logger.info(f"SSE connection closed for document {document_id}")


@router.get("/stream/{document_id}")
async def stream_progress(document_id: str):
    """
    Stream document processing progress via Server-Sent Events.

    Args:
        document_id: Document ID to track

    Returns:
        SSE stream of progress updates
    """
    return StreamingResponse(
        event_generator(document_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )


@router.get("/status/{document_id}")
async def get_progress_status(document_id: str):
    """
    Get current progress status for a document (one-time query, not SSE).

    Args:
        document_id: Document ID

    Returns:
        Current progress data
    """
    tracker = get_progress_tracker()
    progress = tracker.get_progress(document_id)

    if not progress:
        return {
            "document_id": document_id,
            "status": "not_found",
            "message": "No progress data available for this document"
        }

    return progress
