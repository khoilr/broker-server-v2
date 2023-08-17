"""
Init file

Raises:
    Exception: Exception error

Returns:
    None: None
"""
import json
from typing import Union

import gevent.monkey

gevent.monkey.patch_all()
import requests

from server.utils.ssi import config, constants


class SSI(object):
    """Create SSI object.

    Args:
        object (object): object
    """

    def __init__(self, config_file_path: Union[str, None] = None) -> None:
        if config_file_path is None:
            self.config_file_path = "server/utils/ssi/config.py"

        self.config = config
        self.headers = {
            "Authorization": f"{self.config.auth_type} {self.config.access_jwt}",
        }

        self.refresh_token(config_file_path)

    def request(
        self,
        url: str,
        method: str,
        body=None,
        params=None,
        headers=None,
    ) -> dict:
        """
        Request to URL.

        Args:
            url (str): URL
            method (str): request method
            body (_type_, optional): request body. Defaults to None.
            params (_type_, optional): request parameters. Defaults to None.
            headers (_type_, optional): request headers. Defaults to None.

        Returns:
            dict: json response
        """
        body = json.dumps(body)

        if headers is None:
            headers = self.headers

        if method.upper() == "POST":
            return self._post(url, body, params, headers)
        elif method.upper() == "GET":
            return self._get(url, body, params, headers)
        return {"error": "Invalid method"}

    def get_token(self):
        """
        Get token.

        Returns:
            dict: json response
        """
        body = {
            "consumerID": self.config.consumerID,
            "consumerSecret": self.config.consumerSecret,
        }
        auth_type = self.config.auth_type
        access_jwt = self.config.access_jwt
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{auth_type} {access_jwt}",
        }

        return self.request(
            url=constants.ACCESS_TOKEN,
            method="post",
            body=body,
            headers=headers,
        )

    def refresh_token(self, config_file_path: Union[str, None] = None):
        """
        Get new JWT token, reassigned to config and write to file.

        Args:
            config_file_path (Union[str, None]): file to write new config to. Defaults to None.

        Raises:
            Exception: Exception
        """
        token = self.get_token()["data"]["accessToken"]
        if token is not None:
            # Set the access token in the config
            self.config.access_jwt = token

            if config_file_path is None:
                config_file_path = self.config_file_path

            # Write the config to file
            with open(config_file_path, "w") as file:
                [
                    file.write(f'{key} = "{value}"\n')
                    for key, value in self.config.__dict__.items()
                    if not key.startswith("__")
                ]

        else:
            raise Exception("Failed to get access token")

    def _get(
        self,
        url: str,
        body=None,
        params=None,
        headers=None,
    ) -> dict:
        """
        Get request to URL.

        Args:
            url (str): URL
            body (_type_, optional): request body. Defaults to None.
            params (_type_, optional): request parameters. Defaults to None.
            headers (_type_, optional): request headers. Defaults to None.

        Returns:
            dict: json return
        """
        res = requests.get(
            self.config.url + url,
            params=params,
            headers=headers,
            data=body,
            timeout=10,
        )
        return json.loads(res.content)

    def _post(
        self,
        url: str,
        body=None,
        params=None,
        headers=None,
    ) -> dict:
        """
        Post request to URL.

        Args:
            url (str): URL
            body (_type_, optional): request body. Defaults to None.
            params (_type_, optional): request parameters. Defaults to None.
            headers (_type_, optional): request headers. Defaults to None.

        Returns:
            dict: json response
        """
        res = requests.post(
            self.config.url + url,
            params=params,
            headers=headers,
            data=body,
            timeout=10,
        )
        return json.loads(res.content)

    # selected_channel = "B:ALL"
    # market_data_stream = MarketDataStream(on_message=lambda x: print(json.loads(x)), on_error=lambda x: print(x))
    # market_data_stream.start(selected_channel)
