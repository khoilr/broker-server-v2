import inspect
import json

from talipp import indicators

from server.db.dao.predefined_indicator import PredefinedIndicatorDAO
from server.db.dao.predefined_param import PredefinedParamDAO
from server.db.dao.predefined_return import PredefinedReturnDAO
from server.db.dao.stock import StockDAO
from server.db.models.predefined_indicator import PredefinedIndicatorModel
from server.utils.ssi.DataClient import DataClient


async def insert_predefined_indicators():
    with open(
        "server/static/data/predefined_indicators.json",
        "r",
    ) as f:
        data = json.load(f)

    predefined_indicator_dao = PredefinedIndicatorDAO()
    predefined_param_dao = PredefinedParamDAO()
    predefined_return_dao = PredefinedReturnDAO()

    for indicator_name in dir(indicators):
        if indicator_name.startswith("_") or indicator_name == "PivotsHL":
            continue

        if indicator_name not in ["FibRetracement", "Indicator"]:
            (
                predefined_indicator,
                created,
            ) = await predefined_indicator_dao.get_or_create(
                name=indicator_name,
                label=inspect.getdoc(getattr(indicators, indicator_name)).split("\n")[0],  # type: ignore
            )
            # if created:
            #     print(f"Created indicator {indicator_name}")
            # else:
            #     print(f"Found indicator {indicator_name}")

            await insert_predefined_params(
                predefined_indicator=predefined_indicator,
                indicator_name=indicator_name,
                predefined_param_dao=predefined_param_dao,
            )
            await insert_predefined_returns(
                predefined_indicator=predefined_indicator,
                indicator_name=indicator_name,
                predefined_return_dao=predefined_return_dao,
                data=data,
            )


async def insert_predefined_params(
    predefined_indicator: PredefinedIndicatorModel,
    indicator_name: str,
    predefined_param_dao: PredefinedParamDAO,
):
    parameters = inspect.signature(getattr(indicators, indicator_name)).parameters
    for parameter_name in parameters:
        if parameter_name not in ["input_indicator", "value_extractor"]:
            _, created = await predefined_param_dao.get_or_create(
                name=parameter_name,
                label=" ".join(parameter_name.split("_")).title(),
                predefined_indicator=predefined_indicator,
                _type=str(parameters[parameter_name])
                .split(":")[1]
                .split("=")[0]
                .strip(),
            )
            # if created:
            #     print(f"Created parameter {parameter_name} for indicator {indicator_name}")
            # else:
            #     print(f"Found parameter {parameter_name} for indicator {indicator_name}")


async def insert_predefined_returns(
    predefined_indicator: PredefinedIndicatorModel,
    indicator_name: str,
    predefined_return_dao: PredefinedReturnDAO,
    data,
):
    indicator_json = next(
        (item for item in data if item["name"] == indicator_name),
        None,
    )
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
    stock_dao = StockDAO()

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
                page_size=1000,
            )
            stocks = data["data"]
            stock_count += len(stocks)
            total_records = data["totalRecord"]

            for stock in stocks:
                symbol = stock["Symbol"]

                if stock["StockName"] is None or stock["StockEnName"] is None:
                    continue

                try:
                    _, created = await stock_dao.get_or_create(
                        market=market,
                        symbol=symbol,
                        name=stock["StockName"],
                        en_name=stock["StockEnName"],
                    )
                    # if created:
                    #     print(f"Created Stock instance for {symbol} in {market}")
                    # else:
                    #     print(f"Found Stock instance for {symbol} in {market}")
                except Exception as e:
                    print(e)
                    print(stock)

            if stock_count >= total_records:
                break
            else:
                index += 1


async def insert_data():
    await insert_predefined_indicators()
    await insert_stock()
