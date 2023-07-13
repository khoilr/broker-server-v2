import json
import time
from typing import Callable

import signalr
from requests import Session

from server.utils.ssi import SSI


class MarketDataStream(SSI):
    def __init__(
        self,
        on_message: Callable,
        on_error: Callable,
        config_file_path: str = None,
    ):
        super().__init__(config_file_path)

        self.on_message = on_message
        self.on_error = on_error
        self.headers = {
            "Authorization": f"{self.config.auth_type} {self.config.access_jwt}",
        }

    def start(self, channel: str):
        with Session() as session:
            session.headers.update(self.headers)

            connection = signalr.Connection(
                # url=f"{self.config.stream_url}v2.0/signalr",
                url=f"https://fc-data.ssi.com.vn/v2.0/signalr",
                session=session,
            )
            hub = connection.register_hub("FcMarketDataV2Hub")

            hub.client.on("Broadcast", handler=self.on_message)
            hub.client.on("Error", handler=self.on_error)

            connection.start()
            hub.server.invoke("SwitchChannels", channel)

            while True:
                try:
                    connection.wait()
                except:
                    print("Connection lost: Try to reconnect to server!")
                    time.sleep(5)


if __name__ == "__main__":
    selected_channel = "B:ALL"
    market_data_stream = MarketDataStream(
        on_message=lambda x: print(json.loads(x)),
        on_error=lambda x: print(x),
    )
    market_data_stream.start(selected_channel)
