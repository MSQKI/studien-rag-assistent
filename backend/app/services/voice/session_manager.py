"""
Voice Session Manager
Manages active voice study sessions and their state.
"""

import asyncio
import uuid
from datetime import datetime
from typing import Dict, Optional

from loguru import logger

from app.services.voice.realtime_client import RealtimeClient
from app.config import get_settings


class VoiceSession:
    """
    Represents an active voice study session.
    """

    def __init__(self, session_id: str, user_id: str | None = None):
        """
        Initialize a voice session.

        Args:
            session_id: Unique session identifier
            user_id: Optional user identifier
        """
        self.session_id = session_id
        self.user_id = user_id
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        self.client: Optional[RealtimeClient] = None
        self.current_flashcard: Optional[Dict] = None
        self.stats = {
            "cards_reviewed": 0,
            "correct_answers": 0,
            "incorrect_answers": 0,
            "concepts_explained": 0
        }

    async def start(self) -> None:
        """
        Start the realtime connection.
        """
        settings = get_settings()
        self.client = RealtimeClient(settings.openai_api_key)

        # Register event handlers
        self.client.on("response.audio.delta", self._handle_audio_delta)
        self.client.on("response.text.delta", self._handle_text_delta)
        self.client.on("response.function_call_arguments.delta", self._handle_function_call)
        self.client.on("error", self._handle_error)

        await self.client.connect()
        logger.info(f"Started voice session: {self.session_id}")

    async def stop(self) -> None:
        """
        Stop the session and disconnect.
        """
        if self.client:
            await self.client.disconnect()
        logger.info(f"Stopped voice session: {self.session_id}")

    def update_activity(self) -> None:
        """
        Update last activity timestamp.
        """
        self.last_activity = datetime.utcnow()

    async def _handle_audio_delta(self, event: Dict) -> None:
        """
        Handle audio response chunks.

        Args:
            event: Audio delta event
        """
        self.update_activity()
        # Audio will be forwarded to the client WebSocket
        logger.debug(f"Audio delta received for session {self.session_id}")

    async def _handle_text_delta(self, event: Dict) -> None:
        """
        Handle text response chunks.

        Args:
            event: Text delta event
        """
        self.update_activity()
        logger.debug(f"Text delta: {event.get('delta', '')}")

    async def _handle_function_call(self, event: Dict) -> None:
        """
        Handle function call from the model.

        Args:
            event: Function call event
        """
        self.update_activity()
        logger.info(f"Function call in session {self.session_id}: {event}")
        # Function calls will be handled by the session manager

    async def _handle_error(self, event: Dict) -> None:
        """
        Handle error events.

        Args:
            event: Error event
        """
        logger.error(f"Error in session {self.session_id}: {event}")


class SessionManager:
    """
    Manages all active voice sessions.
    """

    def __init__(self):
        """
        Initialize the session manager.
        """
        self.sessions: Dict[str, VoiceSession] = {}
        self.cleanup_task: Optional[asyncio.Task] = None
        self.settings = get_settings()

    async def start_cleanup_task(self) -> None:
        """
        Start background task to clean up expired sessions.
        """
        self.cleanup_task = asyncio.create_task(self._cleanup_loop())

    async def stop_cleanup_task(self) -> None:
        """
        Stop the cleanup task.
        """
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass

    async def _cleanup_loop(self) -> None:
        """
        Periodically clean up expired sessions.
        """
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                await self._cleanup_expired_sessions()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in cleanup loop: {e}")

    async def _cleanup_expired_sessions(self) -> None:
        """
        Remove sessions that have been inactive for too long.
        """
        timeout_minutes = self.settings.session_timeout_minutes
        now = datetime.utcnow()

        expired_sessions = []
        for session_id, session in self.sessions.items():
            inactive_minutes = (now - session.last_activity).total_seconds() / 60
            if inactive_minutes > timeout_minutes:
                expired_sessions.append(session_id)

        for session_id in expired_sessions:
            await self.remove_session(session_id)
            logger.info(f"Removed expired session: {session_id}")

    async def create_session(self, user_id: str | None = None) -> VoiceSession:
        """
        Create a new voice session.

        Args:
            user_id: Optional user identifier

        Returns:
            New VoiceSession instance
        """
        session_id = str(uuid.uuid4())
        session = VoiceSession(session_id, user_id)
        await session.start()

        self.sessions[session_id] = session
        logger.info(f"Created session {session_id} for user {user_id}")

        return session

    async def get_session(self, session_id: str) -> Optional[VoiceSession]:
        """
        Get an active session by ID.

        Args:
            session_id: Session identifier

        Returns:
            VoiceSession if found, None otherwise
        """
        return self.sessions.get(session_id)

    async def remove_session(self, session_id: str) -> None:
        """
        Remove and stop a session.

        Args:
            session_id: Session identifier
        """
        session = self.sessions.pop(session_id, None)
        if session:
            await session.stop()
            logger.info(f"Removed session: {session_id}")

    def get_all_sessions(self) -> list[Dict]:
        """
        Get information about all active sessions.

        Returns:
            List of session information dictionaries
        """
        return [
            {
                "session_id": session.session_id,
                "user_id": session.user_id,
                "created_at": session.created_at.isoformat(),
                "last_activity": session.last_activity.isoformat(),
                "stats": session.stats
            }
            for session in self.sessions.values()
        ]


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """
    Get the global session manager instance.

    Returns:
        SessionManager instance
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
