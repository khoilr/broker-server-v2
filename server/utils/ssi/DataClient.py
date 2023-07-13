from server.utils.ssi import SSI, constants


class DataClient(SSI):
    def __init__(self, config_file_path: str = None):
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
        return super().request(
            url=url,
            method=method,
            body=body,
            params=params,
            headers=self.headers,
        )

    def stocks(self, market: str, page_index: int, page_size: int):
        """
        Get stocks data from SSI

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

    # def securities_details(self, _input_data, _object):
    #     return self._get(const.MD_SECURITIES_DETAILS, body=_input_data, params=_object)

    # def index_components(self, _input_data, _object):
    #     return self._get(const.MD_INDEX_COMPONENTS, body=_input_data, params=_object)

    # def index_list(self, _input_data, _object):
    #     return self._get(const.MD_INDEX_LIST, body=_input_data, params=_object)

    def daily_ohlc(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        page_index: int,
        page_size: int,
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
            _type_: _description_
        """
        params = {
            "symbol": symbol,
            "fromDate": from_date,
            "toDate": to_date,
            "pageIndex": page_index,
            "pageSize": page_size,
            "ascending": ascending,
        }
        return self.this_request(
            constants.MD_DAILY_OHLC,
            method="get",
            params=params,
        )

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
        Get intraday OHLC data from SSI

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
        params = {
            "symbol": symbol,
            "fromDate": from_date,
            "toDate": to_date,
            "resolution": 1,
            "ascending": ascending,
            "pageIndex": page_index,
            "pageSize": page_size,
        }
        return self.this_request(
            url=constants.MD_INTRADAY_OHLC,
            method="get",
            params=params,
        )

    # def daily_index(self, _input_data, _object):
    #     return self._get(const.MD_DAILY_INDEX, body=_input_data, params=_object)

    # def daily_stock_price(self, _input_data, _object):
    #     return self._get(const.MD_DAILY_STOCK_PRICE, body=_input_data, params=_object)

    # def backtest(self, _input_data, _object):
    #     return self._get(const.MD_BACKTEST, body=_input_data, params=_object)


if __name__ == "__main__":
    market_data_client = DataClient()
    print(
        market_data_client.stocks(
            market="HOSE",
            page_index=1,
            page_size=10,
        ),
    )
