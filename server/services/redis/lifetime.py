from fastapi import FastAPI
from redis.asyncio import ConnectionPool

from server.settings import settings


def init_redis(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection pool for redis.

    Args:
        app (FastAPI): current fastapi application.
    """
    app.state.redis_pool = ConnectionPool.from_url(
        str(settings.redis_url),
    )


async def shutdown_redis(app: FastAPI) -> None:  # pragma: no cover
    """
    Closes redis connection pool.

    Args:
        app (FastAPI): current FastAPI app.
    """
    await app.state.redis_pool.disconnect()
