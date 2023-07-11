import asyncio
import inspect
import json

# import ssi_fc_data
from talipp import indicators
from server.utils.ssi.DataClient import DataClient

# from server.utils.ssi import config
from server.db.dao.predefined_indicator_dao import PredefinedIndicatorDAO
from server.db.dao.predefined_param_dao import PredefinedParamDAO
from server.db.dao.predefined_return_dao import PredefinedReturnDAO
from server.db.dao.stock_dao import StockDAO


async def insert_predefined_data():
    with open(
        "server/data/predefined_indicators.json",
        "r",
    ) as f:
        data = json.load(f)

    for indicator_name in dir(indicators):
        if indicator_name.startswith("_") or indicator_name == "PivotsHL":
            continue

        predefined_indicator_dao = PredefinedIndicatorDAO()
        if indicator_name not in ["FibRetracement", "Indicator"]:
            predefined_indicator, created = await predefined_indicator_dao.get_or_create(
                name=indicator_name,
                label=inspect.getdoc(getattr(indicators, indicator_name)).split("\n")[0],
            )
            # if created:
            #     print(f"Created indicator {indicator_name}")
            # else:
            #     print(f"Found indicator {indicator_name}")

            predefined_param_dao = PredefinedParamDAO()
            parameters = inspect.signature(getattr(indicators, indicator_name)).parameters
            for parameter_name in parameters:
                if parameter_name not in ["input_indicator", "value_extractor"]:
                    _, created = await predefined_param_dao.get_or_create(
                        name=parameter_name,
                        label=" ".join(parameter_name.split("_")).title(),
                        predefined_indicator=predefined_indicator,
                        _type=str(parameters[parameter_name]).split(":")[1].split("=")[0].strip(),
                    )
                    # if created:
                    #     print(f"Created parameter {parameter_name} for indicator {indicator_name}")
                    # else:
                    #     print(f"Found parameter {parameter_name} for indicator {indicator_name}")

            predefined_return_dao = PredefinedReturnDAO()
            indicator_json = next((item for item in data if item["name"] == indicator_name), None)
            if indicator_json is not None:
                returns = indicator_json["returns"]

                for _return in returns:
                    name = _return["name"]
                    label = _return["label"]
                    _, created = await predefined_return_dao.create_or_get(
                        name=name,
                        label=label,
                        predefined_indicator=predefined_indicator,
                    )
                    # if created:
                    #     print(f"Created return {name} for indicator {indicator_name}")
                    # else:
                    #     print(f"Found return {name} for indicator {indicator_name}")


async def insert_stock():
    markets = ["HOSE", "HNX", "UPCOM"]

    data_client = DataClient()

    # Insert stock from each market
    for market in markets:
        index = 1
        stock_count = 0

        # Get all stocks from the market
        while True:
            # Get the stock list
            data = data_client.stocks(
                market=market,
                page_index=index,
                page_size=100,
            )
            stocks = data["data"]
            stock_count += len(stocks)
            total_records = data["totalRecord"]

            for stock in stocks:
                symbol = stock["Symbol"]

                if stock["StockName"] is None or stock["StockEnName"] is None:
                    continue

                _, created = await StockDAO().get_or_create(
                    market=market,
                    symbol=symbol,
                    name=stock["StockName"],
                    en_name=stock["StockEnName"],
                )
                # if created:
                #     print(f"Created Stock instance for {symbol} in {market}")
                # else:
                #     print(f"Found Stock instance for {symbol} in {market}")

            if stock_count >= total_records:
                break
            else:
                index += 1


async def insert_data():
    await insert_predefined_data()
    await insert_stock()
