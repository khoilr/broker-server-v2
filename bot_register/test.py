

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from loguru import logger

TOKEN = '6354497790:AAFZ7Ck0PpiPiLgFzYnNpNzX48nKMomhPAY'

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)
    dp.middleware.setup(LoggingMiddleware())

    bot_info = await bot.get_me()
    logger.info(f"Bot info: {bot_info}")

    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):
        await message.reply("Hello! I'm your bot. Send me a message.")

    @dp.message_handler()
    async def echo(message: types.Message):
        await message.answer(message.text)

    await dp.start_polling()

if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
