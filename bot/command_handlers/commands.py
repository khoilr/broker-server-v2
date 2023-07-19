from aiogram.types import Message
from loguru import logger

from server.db.dao.telegram import TelegramDAO


async def start(message: Message):
    user = message.from_user.values

    telegram_dao = TelegramDAO()
    (telegram, created) = await telegram_dao.get_or_create(**user)

    logger.info(f"Telegram: {telegram.__dict__}, created: {created}")

    await message.bot.send_message(
        chat_id=user["id"],
        text="Hello and welcome to Stock Alert Bot! I’m here to help you find the best opportunities in the stock market based on your preferences and goals. You can set up your own trading strategy and I will notify you whenever a stock meets your criteria. Whether you are a beginner or an expert, I will make sure you don’t miss any chance to grow your portfolio. Let’s get started!",
    )
