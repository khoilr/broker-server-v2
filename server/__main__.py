import asyncio
import os
import shutil

import uvicorn

from server.__rocketry__ import app as app_rocketry
from server.settings import settings


def set_multiproc_dir() -> None:
    """
    Sets mutiproc_dir env variable.

    This function cleans up the multiprocess directory
    and recreates it. This actions are required by prometheus-client
    to share metrics between processes.

    After cleanup, it sets two variables.
    Uppercase and lowercase because different
    versions of the prometheus-client library
    depend on different environment variables,
    so I've decided to export all needed variables,
    to avoid undefined behaviour.
    """
    shutil.rmtree(settings.prometheus_dir, ignore_errors=True)
    os.makedirs(settings.prometheus_dir, exist_ok=True)
    os.environ["prometheus_multiproc_dir"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.prometheus_dir.expanduser().absolute(),
    )


class Server(uvicorn.Server):
    """
    Customized uvicorn.Server.

    Uvicorn server overrides signals and we need to include

    Rocketry to the signals.
    """

    def handle_exit(self, sig: int, frame) -> None:
        """
        Handle the exit method.

        Args:
            sig (int): sig
            frame (_type_): frame

        Returns:
            None: None
        """
        app_rocketry.session.shut_down()
        return super().handle_exit(sig, frame)


async def main() -> None:
    """Entrypoint of the application."""
    set_multiproc_dir()
    uvicorn.run(
        "server.web.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        reload_excludes=settings.reload_excludes,
        log_level=settings.log_level.value.lower(),
        factory=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
