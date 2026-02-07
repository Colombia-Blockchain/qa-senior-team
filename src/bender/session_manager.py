"""Session manager — maps Slack threads to Claude Code sessions."""

import logging
import uuid
from asyncio import Lock

logger = logging.getLogger(__name__)


class SessionManager:
    """Thread-safe mapping between Slack thread timestamps and Claude Code session IDs.

    Each Slack thread maps to exactly one Claude Code session,
    enabling multi-turn conversations with context preserved.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, str] = {}
        self._lock = Lock()

    async def create_session(self, thread_ts: str) -> str:
        """Create a new session for a Slack thread.

        Args:
            thread_ts: The Slack thread timestamp identifier.

        Returns:
            The newly generated session ID.
        """
        session_id = str(uuid.uuid4())
        async with self._lock:
            self._sessions[thread_ts] = session_id
        logger.info("Created session %s for thread %s", session_id, thread_ts)
        return session_id

    async def get_session(self, thread_ts: str) -> str | None:
        """Get the session ID for a Slack thread, if one exists.

        Args:
            thread_ts: The Slack thread timestamp identifier.

        Returns:
            The session ID, or None if no session exists for this thread.
        """
        async with self._lock:
            return self._sessions.get(thread_ts)

    async def has_session(self, thread_ts: str) -> bool:
        """Check whether a Slack thread has an existing session.

        Args:
            thread_ts: The Slack thread timestamp identifier.

        Returns:
            True if the thread has an associated session.
        """
        async with self._lock:
            return thread_ts in self._sessions

    async def set_session(self, thread_ts: str, session_id: str) -> None:
        """Explicitly set the session ID for a thread (e.g., from API-created sessions).

        Args:
            thread_ts: The Slack thread timestamp identifier.
            session_id: The Claude Code session ID to associate.
        """
        async with self._lock:
            self._sessions[thread_ts] = session_id
        logger.info("Set session %s for thread %s", session_id, thread_ts)
