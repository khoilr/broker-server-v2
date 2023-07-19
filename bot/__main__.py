import asyncio
import os
from concurrent import futures
from datetime import datetime

from bot.command_handlers import command_handlers
from dotenv import load_dotenv
from loguru import logger
from tortoise import Tortoise

from server.db.config import TORTOISE_CONFIG

# from bot.notify import notification

# Load environment variables
load_dotenv()


async def main():
    # Logging
    logger.add(f"logs/bot-{int(datetime.now().timestamp())}.log")

    # Init tortoise orm
    await Tortoise.init(config=TORTOISE_CONFIG)
    logger.info(f"Tortoise ORM started, connection: {TORTOISE_CONFIG['connections']}")

    cm = await command_handlers()

    # # Run notification task in a separate thread
    # with futures.ThreadPoolExecutor() as pool:
    #     loop = asyncio.get_event_loop()
    #     notification_task = loop.run_in_executor(pool, notification, bot)

    # Run tasks
    await asyncio.gather(
        cm,
        # notification_task,
    )


if __name__ == "__main__":
    asyncio.run(main())
