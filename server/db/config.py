from typing import List

from server.settings import settings

MODELS_MODULES: List[str] = [
    "server.db.models.dummy_model",
    "server.db.models.user_model",
    "server.db.models.telegram_model",
    "server.db.models.whatsapp_model",
    "server.db.models.strategy_model",
    "server.db.models.stock_model",
    "server.db.models.predefined_indicator_model",
    "server.db.models.predefined_param_model",
    "server.db.models.predefined_return_model",
    "server.db.models.indicator_model",
    "server.db.models.param_model",
    "server.db.models.condition_model",
]  # noqa: WPS407

TORTOISE_CONFIG = {  # noqa: WPS407
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default",
        },
    },
}
