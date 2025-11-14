"""
Progress Tracking for Document Processing
Simple in-memory progress tracking with SSE support.
"""

from typing import Dict, Any
from datetime import datetime
import asyncio


class ProgressTracker:
    """Tracks document processing progress for SSE streaming."""

    def __init__(self):
        """Initialize progress tracker."""
        self._progress: Dict[str, Dict[str, Any]] = {}
        self._queues: Dict[str, list] = {}  # SSE queues per document

    def create_progress(self, document_id: str, filename: str) -> None:
        """
        Create a new progress entry for a document.

        Args:
            document_id: Document ID
            filename: Filename
        """
        self._progress[document_id] = {
            "document_id": document_id,
            "filename": filename,
            "status": "started",
            "step": "Initialisierung",
            "progress": 0,
            "total_steps": 4,
            "current_step": 0,
            "started_at": datetime.now().isoformat(),
            "details": ""
        }
        self._queues[document_id] = []

    def update_progress(
        self,
        document_id: str,
        step: str,
        progress: int,
        current_step: int,
        details: str = ""
    ) -> None:
        """
        Update progress for a document.

        Args:
            document_id: Document ID
            step: Current step description
            progress: Progress percentage (0-100)
            current_step: Current step number (1-4)
            details: Additional details
        """
        if document_id in self._progress:
            self._progress[document_id].update({
                "step": step,
                "progress": progress,
                "current_step": current_step,
                "details": details,
                "status": "processing"
            })

            # Notify all SSE listeners
            event_data = self._progress[document_id].copy()
            if document_id in self._queues:
                for queue in self._queues[document_id]:
                    asyncio.create_task(queue.put(event_data))

    def complete_progress(self, document_id: str, results: Dict[str, Any]) -> None:
        """
        Mark progress as complete.

        Args:
            document_id: Document ID
            results: Processing results
        """
        if document_id in self._progress:
            self._progress[document_id].update({
                "status": "completed",
                "step": "Abgeschlossen",
                "progress": 100,
                "current_step": 4,
                "completed_at": datetime.now().isoformat(),
                "results": results
            })

            # Notify SSE listeners
            event_data = self._progress[document_id].copy()
            if document_id in self._queues:
                for queue in self._queues[document_id]:
                    asyncio.create_task(queue.put(event_data))

    def error_progress(self, document_id: str, error: str) -> None:
        """
        Mark progress as failed.

        Args:
            document_id: Document ID
            error: Error message
        """
        if document_id in self._progress:
            self._progress[document_id].update({
                "status": "error",
                "step": "Fehler",
                "error": error,
                "completed_at": datetime.now().isoformat()
            })

            # Notify SSE listeners
            event_data = self._progress[document_id].copy()
            if document_id in self._queues:
                for queue in self._queues[document_id]:
                    asyncio.create_task(queue.put(event_data))

    def get_progress(self, document_id: str) -> Dict[str, Any] | None:
        """
        Get current progress for a document.

        Args:
            document_id: Document ID

        Returns:
            Progress data or None
        """
        return self._progress.get(document_id)

    async def subscribe(self, document_id: str) -> asyncio.Queue:
        """
        Subscribe to progress updates for a document.

        Args:
            document_id: Document ID

        Returns:
            Queue that will receive progress updates
        """
        queue = asyncio.Queue()

        if document_id not in self._queues:
            self._queues[document_id] = []

        self._queues[document_id].append(queue)

        # Send current progress immediately if exists
        if document_id in self._progress:
            await queue.put(self._progress[document_id].copy())

        return queue

    def unsubscribe(self, document_id: str, queue: asyncio.Queue) -> None:
        """
        Unsubscribe from progress updates.

        Args:
            document_id: Document ID
            queue: Queue to remove
        """
        if document_id in self._queues and queue in self._queues[document_id]:
            self._queues[document_id].remove(queue)

    def cleanup(self, document_id: str) -> None:
        """
        Cleanup progress data for a document.

        Args:
            document_id: Document ID
        """
        # Keep completed/error states for 1 hour, remove from memory after
        if document_id in self._progress:
            status = self._progress[document_id].get("status")
            if status in ["completed", "error"]:
                # In production, you'd use a TTL cache or database
                # For now, just keep it in memory
                pass


# Global progress tracker instance
_progress_tracker: ProgressTracker | None = None


def get_progress_tracker() -> ProgressTracker:
    """
    Get global progress tracker instance.

    Returns:
        ProgressTracker instance
    """
    global _progress_tracker
    if _progress_tracker is None:
        _progress_tracker = ProgressTracker()
    return _progress_tracker
