import asyncio
from concurrent import futures
from datetime import datetime

from bot.command_handlers import command_handlers
from dotenv import load_dotenv
from loguru import logger
from tortoise import Tortoise
from bot.notify import notification

from server.db.config import TORTOISE_CONFIG

# Load environment variables
load_dotenv()


async def main():
    """Run main."""
    # Logging
    timestamp = int(datetime.now().timestamp())
    logger.add(f"logs/bot-{timestamp}.log")

    # Init tortoise orm
    await Tortoise.init(config=TORTOISE_CONFIG)
    logger.info(f"Tortoise ORM started, connection: {TORTOISE_CONFIG['connections']}")

    cm = await command_handlers()

    with futures.ThreadPoolExecutor() as pool:
        loop = asyncio.get_event_loop()
        notification_task = loop.run_in_executor(pool, notification)

    # Run tasks
    await asyncio.gather(
        *[cm, notification_task]
    )


if __name__ == "__main__":
    asyncio.run(main())
