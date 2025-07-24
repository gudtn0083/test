import asyncio
import contextlib
from typing import Optional

from .base import ChatProtocol


class TCPProtocol(ChatProtocol):
    """Simple TCP chat protocol using a central server that echoes to clients."""

    def __init__(
        self,
        username: str,
        channel: str = "default",
        host: str = "127.0.0.1",
        port: int = 9009,
    ):
        super().__init__(username, channel)
        self.host = host
        self.port = port
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._reader_task: Optional[asyncio.Task] = None

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port)
        # send join message to identify user
        await self.send(f"** {self.username} joined the chat **")

        async def _listen():
            while True:
                data = await self._reader.readline()
                if not data:
                    break
                try:
                    payload = data.decode().rstrip("\n")
                except UnicodeDecodeError:
                    continue
                await self._dispatch_message(payload)

        self._reader_task = asyncio.create_task(_listen())

    async def send(self, message: str):
        if not self._writer:
            raise RuntimeError("TCP connection not established")
        payload = f"{self.username}: {message}\n"
        self._writer.write(payload.encode())
        await self._writer.drain()

    async def close(self):
        if self._writer:
            self._writer.close()
            with contextlib.suppress(Exception):
                await self._writer.wait_closed()
        if self._reader_task:
            self._reader_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._reader_task