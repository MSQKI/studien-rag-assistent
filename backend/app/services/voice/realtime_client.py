"""
OpenAI Realtime API Client for Voice Study Buddy.
Handles WebSocket connection to OpenAI Realtime API.
"""

import asyncio
import json
from typing import Dict, Any, Callable, Optional
from enum import Enum

import websockets
from loguru import logger

from app.config import get_settings


class RealtimeEventType(str, Enum):
    """Realtime API event types."""
    SESSION_UPDATE = "session.update"
    SESSION_CREATED = "session.created"
    INPUT_AUDIO_BUFFER_APPEND = "input_audio_buffer.append"
    INPUT_AUDIO_BUFFER_COMMIT = "input_audio_buffer.commit"
    RESPONSE_CREATE = "response.create"
    RESPONSE_CANCEL = "response.cancel"
    CONVERSATION_ITEM_CREATE = "conversation.item.create"
    CONVERSATION_ITEM_DELETE = "conversation.item.delete"

    # Server events
    ERROR = "error"
    RESPONSE_AUDIO_DELTA = "response.audio.delta"
    RESPONSE_AUDIO_DONE = "response.audio.done"
    RESPONSE_TEXT_DELTA = "response.text.delta"
    RESPONSE_TEXT_DONE = "response.text.done"
    RESPONSE_FUNCTION_CALL = "response.function_call_arguments.delta"
    CONVERSATION_ITEM_CREATED = "conversation.item.created"


class RealtimeClient:
    """
    Client for OpenAI Realtime API.
    Manages WebSocket connection and event handling.
    """

    def __init__(self, api_key: str):
        """
        Initialize Realtime API client.

        Args:
            api_key: OpenAI API key
        """
        self.settings = get_settings()
        self.api_key = api_key
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.event_handlers: Dict[str, list[Callable]] = {}
        self.is_connected = False
        self._receive_task: Optional[asyncio.Task] = None

    async def connect(self) -> None:
        """
        Connect to OpenAI Realtime API via WebSocket.
        """
        url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "realtime=v1"
        }

        try:
            self.ws = await websockets.connect(url, extra_headers=headers)
            self.is_connected = True
            logger.info("Connected to OpenAI Realtime API")

            # Send initial session configuration
            await self._configure_session()

            # Start receiving messages
            self._receive_task = asyncio.create_task(self._receive_messages())

        except Exception as e:
            logger.error(f"Failed to connect to Realtime API: {str(e)}")
            raise

    async def disconnect(self) -> None:
        """
        Disconnect from Realtime API.
        """
        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass

        if self.ws:
            await self.ws.close()
            self.is_connected = False
            logger.info("Disconnected from Realtime API")

    async def _configure_session(self) -> None:
        """
        Send initial session configuration.
        """
        session_config = {
            "type": RealtimeEventType.SESSION_UPDATE,
            "session": {
                "modalities": ["text", "audio"],
                "instructions": (
                    "Du bist ein freundlicher Studienassistent. "
                    "Du hilfst Studierenden beim Lernen mit Karteikarten und erklärst Konzepte. "
                    "Antworte immer auf Deutsch. Sei geduldig und ermutigend."
                ),
                "voice": self.settings.voice_name,
                "input_audio_format": self.settings.audio_format,
                "output_audio_format": self.settings.audio_format,
                "input_audio_transcription": {
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": self.settings.turn_detection_type,
                    "threshold": self.settings.vad_threshold,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": self.settings.vad_silence_duration_ms
                },
                "tools": [
                    {
                        "type": "function",
                        "name": "get_flashcard",
                        "description": "Holt die nächste Karteikarte für den Studenten",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "subject": {
                                    "type": "string",
                                    "description": "Fachgebiet (optional)"
                                }
                            }
                        }
                    },
                    {
                        "type": "function",
                        "name": "check_answer",
                        "description": "Überprüft die Antwort des Studenten auf eine Karteikarte",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "flashcard_id": {
                                    "type": "string",
                                    "description": "ID der Karteikarte"
                                },
                                "user_answer": {
                                    "type": "string",
                                    "description": "Antwort des Studenten"
                                },
                                "correct": {
                                    "type": "boolean",
                                    "description": "War die Antwort korrekt?"
                                }
                            },
                            "required": ["flashcard_id", "correct"]
                        }
                    },
                    {
                        "type": "function",
                        "name": "explain_concept",
                        "description": "Erklärt ein Konzept ausführlich mithilfe der RAG-Dokumentendatenbank",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "concept": {
                                    "type": "string",
                                    "description": "Das zu erklärende Konzept"
                                }
                            },
                            "required": ["concept"]
                        }
                    }
                ]
            }
        }

        await self.send_event(session_config)
        logger.info("Sent session configuration")

    async def send_event(self, event: Dict[str, Any]) -> None:
        """
        Send an event to the Realtime API.

        Args:
            event: Event data to send
        """
        if not self.is_connected or not self.ws:
            raise RuntimeError("Not connected to Realtime API")

        await self.ws.send(json.dumps(event))
        logger.debug(f"Sent event: {event.get('type')}")

    async def _receive_messages(self) -> None:
        """
        Continuously receive and process messages from the API.
        """
        try:
            async for message in self.ws:
                try:
                    event = json.loads(message)
                    event_type = event.get("type")

                    logger.debug(f"Received event: {event_type}")

                    # Call registered handlers
                    if event_type in self.event_handlers:
                        for handler in self.event_handlers[event_type]:
                            await handler(event)

                    # Handle specific events
                    if event_type == RealtimeEventType.ERROR:
                        logger.error(f"Realtime API error: {event}")

                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode message: {e}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

        except asyncio.CancelledError:
            logger.info("Receive task cancelled")
        except Exception as e:
            logger.error(f"Error in receive loop: {e}")

    def on(self, event_type: str, handler: Callable) -> None:
        """
        Register an event handler.

        Args:
            event_type: Type of event to handle
            handler: Async function to call when event occurs
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    async def append_input_audio(self, audio_data: bytes) -> None:
        """
        Append audio data to the input buffer.

        Args:
            audio_data: PCM16 audio data
        """
        import base64

        event = {
            "type": RealtimeEventType.INPUT_AUDIO_BUFFER_APPEND,
            "audio": base64.b64encode(audio_data).decode('utf-8')
        }
        await self.send_event(event)

    async def commit_audio(self) -> None:
        """
        Commit the input audio buffer and trigger response generation.
        """
        await self.send_event({
            "type": RealtimeEventType.INPUT_AUDIO_BUFFER_COMMIT
        })

    async def create_response(self) -> None:
        """
        Manually trigger response generation (for turn_detection: disabled).
        """
        await self.send_event({
            "type": RealtimeEventType.RESPONSE_CREATE
        })

    async def send_text_message(self, text: str) -> None:
        """
        Send a text message to the conversation.

        Args:
            text: Text message to send
        """
        await self.send_event({
            "type": RealtimeEventType.CONVERSATION_ITEM_CREATE,
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": text
                    }
                ]
            }
        })
        await self.create_response()

    async def call_function(self, call_id: str, output: str) -> None:
        """
        Send function call output back to the API.

        Args:
            call_id: Function call ID
            output: Function output (JSON string)
        """
        await self.send_event({
            "type": RealtimeEventType.CONVERSATION_ITEM_CREATE,
            "item": {
                "type": "function_call_output",
                "call_id": call_id,
                "output": output
            }
        })
