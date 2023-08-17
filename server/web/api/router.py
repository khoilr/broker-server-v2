from fastapi.routing import APIRouter

from server.web.api import (
    auth,
    dummy,
    indicator,
    monitoring,
    predefined_indicator,
    predict,
    price,
    redis,
    stock,
    strategy,
)

api_router = APIRouter()

api_router.include_router(monitoring.router)
api_router.include_router(
    dummy.router,
    prefix="/dummy",
    tags=["dummy"],
)
api_router.include_router(
    redis.router,
    prefix="/redis",
    tags=["redis"],
)
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    indicator.router,
    prefix="/indicator",
    tags=["indicator"],
)
api_router.include_router(
    predefined_indicator.router,
    prefix="/predefined_indicator",
    tags=["predefined_indicator"],
)
api_router.include_router(
    price.router,
    prefix="/price",
    tags=["price"],
)
api_router.include_router(
    stock.router,
    prefix="/stock",
    tags=["stock"],
)
api_router.include_router(
    strategy.router,
    prefix="/strategy",
    tags=["strategy"],
)
api_router.include_router(
    predict.router,
    prefix="/predict",
    tags=["predict"],
)
