import asyncio
import contextlib
from typing import Optional

from .base import ChatProtocol

try:
    from cyclonedds.domain import DomainParticipant
    from cyclonedds.topic import Topic
    from cyclonedds.pub import DataWriter
    from cyclonedds.sub import DataReader
    from cyclonedds.idl import IdlString, IdlStruct
except ImportError:  # Package missing – allow graceful degradation
    DomainParticipant = Topic = DataWriter = DataReader = None  # type: ignore


class DDSUnavailableError(RuntimeError):
    pass


if DomainParticipant is not None:

    class _ChatMsg(IdlStruct, typename="ChatMsg"):
        """IDL struct representing a chat message."""

        txt: IdlString(512)

    class DDSProtocol(ChatProtocol):
        """DDS transport implementation using Eclipse CycloneDDS."""

        def __init__(self, username: str, channel: str = "ChatChannel", domain: int = 0):
            super().__init__(username, channel)
            self.domain = domain
            self._participant: Optional[DomainParticipant] = None
            self._writer: Optional[DataWriter] = None
            self._reader: Optional[DataReader] = None
            self._listener_task: Optional[asyncio.Task] = None

        async def connect(self):
            self._participant = DomainParticipant(self.domain)
            self._topic = Topic(self._participant, self.channel, _ChatMsg)
            self._writer = DataWriter(self._participant, self._topic)
            self._reader = DataReader(self._participant, self._topic)

            async def _listen():
                while True:
                    for data, _info in self._reader.take_iter(timeout=0.1):
                        await self._dispatch_message(data.txt)
                    await asyncio.sleep(0.05)

            self._listener_task = asyncio.create_task(_listen())

        async def send(self, message: str):
            if not self._writer:
                raise RuntimeError("DDS writer not initialised")
            payload = _ChatMsg(txt=f"{self.username}: {message}")
            self._writer.write(payload)

        async def close(self):
            if self._listener_task:
                self._listener_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await self._listener_task
            if self._participant:
                self._participant.close()
else:

    class DDSProtocol(ChatProtocol):  # type: ignore
        """Fallback protocol that raises at runtime if DDS not installed."""

        def __init__(self, *args, **kwargs):
            super().__init__(kwargs.get("username", "unknown"), kwargs.get("channel", "chat"))

        async def connect(self):
            raise DDSUnavailableError(
                "cyclonedds Python package is not installed. Install it or remove --protocol dds option."
            )

        async def send(self, message: str):
            raise DDSUnavailableError("DDS protocol unavailable")

        async def close(self):
            pass