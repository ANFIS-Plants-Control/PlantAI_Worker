import asyncio
from src.Server.server import Server


if __name__ == "__main__":
    try:
        asyncio.run(Server().run())
    except KeyboardInterrupt:
        pass
