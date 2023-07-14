from typing import List

from server.settings import settings

MODELS_MODULES: List[str] = [
    "server.db.models.dummy",
    "server.db.models.user",
    "server.db.models.telegram",
    "server.db.models.whatsapp",
    "server.db.models.strategy",
    "server.db.models.stock",
    "server.db.models.predefined_indicator",
    "server.db.models.predefined_param",
    "server.db.models.predefined_return",
    "server.db.models.indicator",
    "server.db.models.param",
    "server.db.models.condition",
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
