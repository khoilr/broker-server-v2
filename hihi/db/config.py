from typing import List

from hihi.settings import settings

MODELS_MODULES: List[str] = [
    "hihi.db.models.dummy_model",
    "hihi.db.models.user_model",
    "hihi.db.models.telegram_model",
    "hihi.db.models.whatsapp_model",
    "hihi.db.models.strategy_model",
    "hihi.db.models.stock_model",
    "hihi.db.models.predefined_indicator_model",
    "hihi.db.models.predefined_param_model",
    "hihi.db.models.predefined_return_model",
    "hihi.db.models.indicator_model",
    "hihi.db.models.param_model",
    "hihi.db.models.condition_model",
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
