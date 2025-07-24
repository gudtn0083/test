import asyncio
from typing import Optional

import paho.mqtt.client as mqtt

from .base import ChatProtocol
import contextlib


class MQTTProtocol(ChatProtocol):
    """MQTT transport implementation (using paho-mqtt)."""

    def __init__(
        self,
        username: str,
        channel: str = "chat/channel",
        host: str = "test.mosquitto.org",
        port: int = 1883,
    ):
        super().__init__(username, channel)
        self.host = host
        self.port = port
        self._client: Optional[mqtt.Client] = None
        # Internal asyncio Queue to bridge thread->asyncio
        self._queue: asyncio.Queue[str] = asyncio.Queue()
        self._reader_task: Optional[asyncio.Task] = None

    # ------------------------------------------------------------------
    async def connect(self):
        loop = asyncio.get_running_loop()
        # paho-mqtt runs in its own threads, but we need to forward messages to asyncio loop.
        def _on_connect(client, userdata, flags, rc):
            client.subscribe(self.channel)

        def _on_message(client, userdata, msg):
            payload = msg.payload.decode()
            # forward to asyncio loop via thread-safe call
            asyncio.run_coroutine_threadsafe(self._queue.put(payload), loop)

        self._client = mqtt.Client(client_id=f"chat_{self.username}")
        self._client.on_connect = _on_connect
        self._client.on_message = _on_message
        self._client.connect(self.host, self.port, keepalive=60)
        self._client.loop_start()

        # Spawn reader task to consume from queue and dispatch to handler
        async def _reader():
            while True:
                payload = await self._queue.get()
                await self._dispatch_message(payload)

        self._reader_task = asyncio.create_task(_reader())

    async def send(self, message: str):
        if not self._client:
            raise RuntimeError("MQTT client not connected")
        payload = f"{self.username}: {message}"
        # publish is thread-safe
        self._client.publish(self.channel, payload)

    async def close(self):
        if self._client:
            self._client.loop_stop()
            self._client.disconnect()
        if self._reader_task:
            self._reader_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._reader_task