import asyncio
from src.Server.server import Server


if __name__ == "__main__":
    asyncio.run(Server().run()) 