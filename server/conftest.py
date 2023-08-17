from typing import AsyncGenerator

import nest_asyncio
import pytest
from fakeredis import FakeServer
from fakeredis.aioredis import FakeConnection
from fastapi import FastAPI
from httpx import AsyncClient
from redis.asyncio import ConnectionPool
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer

from server.db.config import MODELS_MODULES, TORTOISE_CONFIG
from server.services.redis.dependency import get_redis_pool
from server.settings import settings
from server.web.application import get_app

nest_asyncio.apply()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    Returns:
        str: backend name
    """
    return "asyncio"


@pytest.fixture(autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """
    Initialize database.

    Yields:
        None: None
    """
    initializer(
        MODELS_MODULES,
        db_url=str(settings.db_url),
        app_label="models",
    )
    await Tortoise.init(config=TORTOISE_CONFIG)

    yield

    await Tortoise.close_connections()
    finalizer()


@pytest.fixture
async def fake_redis_pool() -> AsyncGenerator[ConnectionPool, None]:
    """
    Get instance of a fake redis.

    Yields:
        Iterator[AsyncGenerator[ConnectionPool, None]]: AsyncGenerator iterator
    """
    server = FakeServer()
    server.connected = True
    pool = ConnectionPool(connection_class=FakeConnection, server=server)

    yield pool

    await pool.disconnect()


@pytest.fixture
def fastapi_app(
    fake_redis_pool: ConnectionPool,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    Returns:
        FastAPI: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_redis_pool] = lambda: fake_redis_pool
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    Args:
        fastapi_app (FastAPI): FastAPI application

    Yields:
        Iterator[AsyncGenerator[AsyncClient, None]]: Asynchronous Client
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
