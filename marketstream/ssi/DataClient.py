from datetime import datetime, timedelta
from typing import Union

from marketstream.ssi import SSI, constants


class DataClient(SSI):
    """
    Data client class.

    Args:
        SSI (SSI): SSI
    """

    def __init__(self, config_file_path: Union[str, None] = None):
        super().__init__(config_file_path)
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"{self.config.auth_type} {self.config.access_jwt}",
        }

    def this_request(
        self,
        url: str,
        method: str,
        body=None,
        params=None,
    ):
        """
        Request to URL.

        Args:
            url (str): URL
            method (str): Request method
            body (_type_, optional): Additional body. Defaults to None.
            params (_type_, optional): Additional parameters. Defaults to None.

        Returns:
            No idea: No idea
        """
        return super().request(
            url=url,
            method=method,
            body=body,
            params=params,
            headers=self.headers,
        )

    def stocks(self, market: str, page_index: int, page_size: int):
        """
        Get stocks data from SSI.

        Args:
            market (str): HOSE, HNX, UPCOM
            page_index (int): index of page
            page_size (int): size of page

        Returns:
            dict: response from SSI
        """
        params = {
            "market": market,
            "pageIndex": page_index,
            "pageSize": page_size,
        }

        return self.this_request(
            url=constants.STOCKS,
            method="get",
            params=params,
        )

    def daily_ohlc(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        page_index: int = 1,
        page_size: int = 100,
        ascending: bool = True,
    ):
        """
        Get daily OHLC data from SSI

        Args:
            symbol (str): symbol of stock
            from_date (str): from date in format dd/mm/yyyy
            to_date (str): to date in format dd/mm/yyyy
            page_index (int): index of page
            page_size (int): size of page
            ascending (bool, optional): sort by ascending. Defaults to True.

        Returns:
            type_: description_
        """
        # Convert the date strings to datetime objects
        from_date = datetime.strptime(from_date, "%d/%m/%Y")
        to_date = datetime.strptime(to_date, "%d/%m/%Y")

        # Generate the 30-day periods
        periods = []
        current_date = from_date

        while current_date < to_date:
            period_end = current_date + timedelta(days=30)
            if period_end > to_date:
                period_end = to_date

            periods.append((current_date, period_end))
            current_date = period_end + timedelta(days=1)

        # Print the generated periods
        data = {}
        data["data"] = []
        for period in periods:
            params = {
                "symbol": symbol,
                "fromDate": period[0].strftime("%d/%m/%Y"),
                "toDate": period[1].strftime("%d/%m/%Y"),
                "pageIndex": page_index,
                "pageSize": page_size,
                "ascending": ascending,
            }
            request = self.this_request(
                constants.MD_DAILY_OHLC,
                method="get",
                params=params,
            )
            for i in request["data"]:
                data["data"].append(i)
        return data

    def intraday_ohlc(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        page_index: int,
        page_size: int,
        ascending: bool = True,
    ):
        """
        Get intraday OHLC data from SSI.

        Args:
            symbol (str): symbol of stock
            from_date (str): from date in format dd/mm/yyyy
            to_date (str): to date in format dd/mm/yyyy
            page_index (int): index of page
            page_size (int): size of page
            ascending (bool): sort by ascending. Defaults to True.

        Returns:
            dict: response from SSI
        """
        # convert from_date to_date to datetime object
        from_date_datetime = datetime.strptime(from_date, "%d/%m/%Y")
        to_date_datetime = datetime.strptime(to_date, "%d/%m/%Y")

        # break down from_date_datetime and to_date_datetime into smaller chunks in 30 days
        response = None
        while from_date_datetime < to_date_datetime:
            # Get min to_date_datetime
            current_to_date_datetime = min(
                from_date_datetime + timedelta(days=30),
                to_date_datetime,
            )

            # Call API
            params = {
                "symbol": symbol,
                "fromDate": from_date_datetime.strftime("%d/%m/%Y"),
                "toDate": current_to_date_datetime.strftime("%d/%m/%Y"),
                "pageIndex": 1,
                "pageSize": 9999,
                "ascending": ascending,
            }
            current_response = self.this_request(
                constants.MD_INTRADAY_OHLC,
                method="get",
                params=params,
            )

            # Merge response
            if response is None:
                response = current_response
            else:
                response["data"] += current_response["data"]
                response["totalRecord"] += current_response["totalRecord"]

            # Update from_date_datetime
            from_date_datetime = current_to_date_datetime + timedelta(days=1)

        # Return response
        return response
