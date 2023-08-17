"""
Command handlers.

Returns:
    None: None
"""

import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.command_handlers.commands import start
from loguru import logger


async def command_handlers() -> asyncio.Task:
    """
    Register handler for message.

    Returns:
        Task: Coroutine
    """
    # Init bot
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = Bot(token=token)  # type: ignore
    logger.info(token)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Log bot info
    bot_info = await bot.get_me()
    logger.info(f"Bot info: {bot_info}")

    # Register command handlers
    dp.register_message_handler(start, commands=["start"])

    return asyncio.create_task(dp.start_polling())
