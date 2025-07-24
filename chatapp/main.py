import argparse
import asyncio
import sys

from .client import ChatClient


def parse_args():
    parser = argparse.ArgumentParser(description="Multi-protocol chat client")
    parser.add_argument("--protocol", choices=["tcp", "mqtt", "dds"], default="tcp")
    parser.add_argument("--username", required=True)
    parser.add_argument("--channel", default="general")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9009)
    parser.add_argument("--mqtt_port", type=int, default=1883)
    parser.add_argument("--domain", type=int, default=0, help="DDS domain id")
    return parser.parse_args()


def main():
    args = parse_args()

    extra = {}
    if args.protocol == "tcp":
        extra = {"host": args.host, "port": args.port}
    elif args.protocol == "mqtt":
        extra = {"host": args.host, "port": args.mqtt_port}
    elif args.protocol == "dds":
        extra = {"domain": args.domain}

    client = ChatClient(
        username=args.username,
        protocol=args.protocol,
        channel=args.channel,
        **extra,
    )

    def print_message(msg: str):
        print(f"\r{msg}\n> ", end="", flush=True)

    client.on_message(print_message)

    async def run_chat():
        await client.start()
        print("Connected! Type messages, Ctrl+C to quit.")
        print("> ", end="", flush=True)
        loop = asyncio.get_running_loop()
        # reading from stdin is blocking; delegate to executor
        while True:
            msg = await loop.run_in_executor(None, sys.stdin.readline)
            if not msg:
                break
            msg = msg.rstrip("\n")
            if msg:
                await client.send(msg)
                print("> ", end="", flush=True)

    try:
        asyncio.run(run_chat())
    except (KeyboardInterrupt, EOFError):
        pass

    print("\nClosing client...")
    try:
        asyncio.run(client.close())
    except RuntimeError:
        # already closed loop
        pass


if __name__ == "__main__":
    main()