import asyncio
from typing import Callable

from .protocols import MQTTProtocol, TCPProtocol, DDSProtocol, ChatProtocol

_PROTOCOL_TABLE = {
    "mqtt": MQTTProtocol,
    "tcp": TCPProtocol,
    "dds": DDSProtocol,
}


class ChatClient:
    """High-level chat client that hides transport details from the user."""

    def __init__(
        self,
        username: str,
        protocol: str = "tcp",
        channel: str = "general",
        **kwargs,
    ):
        if protocol not in _PROTOCOL_TABLE:
            raise ValueError(f"Unsupported protocol '{protocol}'. Choose from {list(_PROTOCOL_TABLE)}")
        self._impl: ChatProtocol = _PROTOCOL_TABLE[protocol](
            username=username, channel=channel, **kwargs
        )
        self._running = False

    def on_message(self, handler: Callable[[str], None]):
        self._impl.set_message_handler(handler)

    async def start(self):
        await self._impl.connect()
        self._running = True

    async def send(self, message: str):
        await self._impl.send(message)

    async def close(self):
        if self._running:
            await self._impl.close()
            self._running = False