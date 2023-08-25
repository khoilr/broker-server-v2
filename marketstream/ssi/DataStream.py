import time
from typing import Callable, Union
# import gevent.monkey
# gevent.monkey.patch_all()
import signalr
from requests import Session
from loguru import logger
import asyncio

from marketstream.ssi import SSI


class MarketDataStream(SSI):
    """
    Market data streaming object.

    Args:
        SSI (SSI): SSI
    """

    def __init__(
        self,
        on_message: Callable,
        on_error: Callable,
        config_file_path: Union[str, None] = None,
    ):
        """
        Initialize market data stream.

        Args:
            on_message (Callable): on message condition
            on_error (Callable): on error condition
            config_file_path (Union[str, None], optional): idk. Defaults to None.
        """
        super().__init__(config_file_path)

        self.on_message = on_message
        self.on_error = on_error
        auth_type = self.config.auth_type
        access_jwt = self.config.access_jwt
        self.headers = {
            "Authorization": f"{auth_type} {access_jwt}",
        }

    async def start(self, channel: str):
        """
        Start market data.

        Args:
            channel (str): market channel
        """
        with Session() as session:
            session.headers.update(self.headers)
            connection = signalr.Connection(
                url="https://fc-data.ssi.com.vn/v2.0/signalr",
                session=session,
            )
            hub = connection.register_hub("FcMarketDataV2Hub")

            def message_handler(message):
                asyncio.run(self.on_message(message))

            def error_handler(error):
                asyncio.run(self.on_error(error))

            hub.client.on("Broadcast", handler=message_handler)
            hub.client.on("Error", handler=error_handler)

            connection.start()
            hub.server.invoke("SwitchChannels", channel)

            while True:
                try:
                    connection.wait()
                except Exception:
                    time.sleep(5)


# if __name__ == "__main__":
#     selected_channel = "B:ALL"
#     market_data_stream = MarketDataStream(
#         on_message=lambda data: print(json.loads(data)),
#         on_error=lambda error: print(error),
#     )
#     market_data_stream.start(selected_channel)
