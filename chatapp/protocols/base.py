import asyncio
from abc import ABC, abstractmethod
from typing import Callable, Optional


class ChatProtocol(ABC):
    """Abstract base class for chat transport protocols."""

    def __init__(self, username: str, channel: str):
        self.username = username
        self.channel = channel
        self._on_message: Optional[Callable[[str], None]] = None

    def set_message_handler(self, handler: Callable[[str], None]):
        """Assign the callback used when a new chat message arrives."""
        self._on_message = handler

    async def _dispatch_message(self, payload: str):
        if self._on_message:
            self._on_message(payload)

    # Life-cycle APIs -----------------------------------------------------
    @abstractmethod
    async def connect(self):
        """Establish connection to the underlying transport/broker/server."""
        raise NotImplementedError

    @abstractmethod
    async def send(self, message: str):
        """Send a message to other peers in *channel*."""
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        """Close any open sockets/broker connections."""
        raise NotImplementedError

    # Convenience ---------------------------------------------------------
    async def aexec(self, coro):
        """Utility: ensure *coro* is awaited in a task when already in loop."""
        loop = asyncio.get_running_loop()
        return await asyncio.ensure_future(coro, loop=loop)