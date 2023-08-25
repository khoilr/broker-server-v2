import asyncio
from concurrent import futures
from datetime import datetime

from dotenv import load_dotenv
from loguru import logger
from tortoise import Tortoise, run_async

from marketstream.notify import notification
from server.db.config import TORTOISE_CONFIG
from server.db.dao.stock import StockDAO
# Load environment variables
load_dotenv()


async def init_db():
    """Run main."""
    # Logging
    timestamp = int(datetime.now().timestamp())
    logger.add(f"logs/bot-{timestamp}.log")

    # Init tortoise orm
    await Tortoise.init(config=TORTOISE_CONFIG)
    logger.info(f"Tortoise ORM started, connection: {TORTOISE_CONFIG['connections']}")

async def main():
    await init_db()
    # stock_dao = StockDAO()
    # stock = await stock_dao.get_by_symbol(symbol="AAA")
    # logger.info(stock.symbol)
    await notification()


if __name__ == "__main__":
    run_async(main())
