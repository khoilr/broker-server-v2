import asyncio
import os
from asyncio import Task

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_register.command_handlers.commands import start
from loguru import logger


async def command_handlers() -> Task:
    # Init bot
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))  # type: ignore
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(LoggingMiddleware())

    # Log bot info
    bot_info = await bot.get_me()
    logger.info(f"Bot info: {bot_info}")

    # Register command handlers
    dp.register_message_handler(start, commands=["start"])
    logger.info("Bot started!")
    await dp.start_polling()
