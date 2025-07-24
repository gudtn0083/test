import argparse
import asyncio
from typing import List


CLIENTS: List[asyncio.StreamWriter] = []


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    CLIENTS.append(writer)
    addr = writer.get_extra_info("peername")
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            # Broadcast to all other clients
            for w in CLIENTS:
                if w is writer:
                    continue
                w.write(data)
            for w in CLIENTS:
                if not w.is_closing():
                    await w.drain()
    finally:
        CLIENTS.remove(writer)
        writer.close()
        await writer.wait_closed()
        print(f"Client {addr} disconnected")


async def main(host: str, port: int):
    server = await asyncio.start_server(handle_client, host, port)
    addr = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Chat TCP server listening on {addr}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple TCP chat server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=9009)
    args = parser.parse_args()

    try:
        asyncio.run(main(args.host, args.port))
    except KeyboardInterrupt:
        print("Server stopped")