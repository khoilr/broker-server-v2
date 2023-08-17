import asyncio
import json
import time
import sys
import os

from talipp.ohlcv import OHLCVFactory
from aiogram import Bot
# Get the current working directory
current_directory = os.getcwd()

# Add the current directory to sys.path
sys.path.append(current_directory)
from server.utils.ssi.DataStream import MarketDataStream
from server.db.dao.strategy import StrategyDAO
from server.db.dao.stock import StockDAO
# from server.db.dao.strategy import StrategyDAO
from server.db.models.strategy import StrategyModel
from server.db.models.indicator import IndicatorModel
from server.db.models.param import ParameterModel
from server.db.models.predefined_param import PredefinedParamModel
from server.db.models.condition import ConditionModel
from server.db.models.predefined_indicator import PredefinedIndicatorModel
from server.db.models.user import UserModel
from server.db.models.telegram import TelegramModel
from talipp import indicators
from dotenv import load_dotenv

load_dotenv()
taS = []
token = os.getenv("TELEGRAM_BOT_TOKEN")
telegram_bot = Bot(token=token)  # type: ignore


async def notification():
    """Notify user"""
    selected_channel = "B:ALL"
    data_stream = MarketDataStream(
        on_message=on_message,
        on_error=on_error,
    )
    data_stream.start(selected_channel)


async def notify(strategy: StrategyModel, notification_string: str):
    """
    Notify the telegram user if strategy's condition is met.

    Args:
        strategy (StrategyModel): Strategy model from db
        notification_string (str): Message to notify
    """
    user: UserModel = strategy.user

    # Telegram
    if user.telegram is not None:
        telegram_account: TelegramModel = user.telegram

        # When telegram user is registered
        if telegram_account.id is not None:
            # Manual commit
            # This is to prevent the database from being locked
            # Send message to telegram
            await telegram_bot.send_message(
                chat_id=telegram_account.id,
                text=notification_string,
            )
            # Modify notified to True
            # notified_strategy["notified"] = True
    else:
        # # Modify notified to False in the list if condition is not met
        # notified_strategy["notified"] = False
        pass


def get_stock_model(symbol):
    """Get stock model."""
    stock_dao = StockDAO()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    stock_object = loop.run_until_complete(stock_dao.get_by_name(symbol=symbol))
    loop.close()
    return stock_object


def get_strategy_models(stock_object):
    """Get strategy models."""
    strategy_dao = StrategyDAO()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    stock_object = loop.run_until_complete(strategy_dao.filter_from_stock(stock=stock_object))
    loop.close()
    return stock_object


def on_message(message: dict):
    """
    Bot response if reveived message.

    Args:
        message (dict): Callable
    """
    global taS
    # try:
    # Get symbol from message
    content = json.loads(message)["Content"]
    symbol = json.loads(content)["Symbol"]
    if symbol is None:
        return

    # check if the symbol exists
    stock_object = get_stock_model(symbol=symbol)
    if stock_object is None:
        return

    strategies = get_strategy_models(stock_object)
    for strategy in strategies:
        strategy: StrategyModel = strategy
        is_met_condition = True
        notification_str = ""

        # loop indicators
        for indicator in strategy.indicators:
            # Annotate indicator
            indicator: IndicatorModel = indicator
            params = get_params(indicator=indicator, content=content)

            condition: ConditionModel = indicator.condition

            # get technical analysis
            output = get_output_ta(
                indicator=indicator,
                params=params,
                source=condition.source,
            )

            is_met_condition = is_meet_condition(output, condition)
            if is_met_condition:
                notification_str += f"{PredefinedIndicatorModel.get(indicators=indicator).name} {condition.change} {condition.value}\n"
                strategy.active = False


            # I literally have no idea what this section is so I let the rest for you to handle

            # else:
            #     for notified_strategy in notified_strategies:
            #         # parse notified_strategy to dict
            #         notified_strategy_dict = json.loads(notified_strategy)

            #         # If strategy is not notified
            #         if (
            #             notified_strategy_dict["id"] == strategy.id
            #             and notified_strategy_dict["active"]
            #         ):
            #             # Modify notified to True
            #             notified_strategy_dict["active"] = False

            #             # Modify the list in redis
            #             # redis_db.lset(
            #             #     symbol,
            #             #     notified_strategies.index(notified_strategy),
            #             #     json.dumps(notified_strategy_dict),
            #             # )

            #             break
        if is_met_condition:
            asyncio.run(notify(strategy=strategy, notification_string=notification_str))

    # except Exception:
    #     pass


def on_error(error):
    print(error)


def is_meet_condition(output, condition: IndicatorModel.condition) -> bool:
    """
    Check if the condition is met

    Args:
        output (any): No idea, maybe the technical analysis value
        condition (IndicatorModel.condition): Indicator condition

    Returns:
        bool: condition is met or not
    """
    if len(output) > 0:
        return (
            True
            if eval(f"{output[-1]} {condition.change} {condition.value}")
            else False
        )
    else:
        return False


class TechnicalAnalysis:
    def __init__(self, name: str, kwargs: dict) -> None:
        self.func = getattr(indicators, name)
        self.func = self.func(**kwargs)

    def compose(self):
        return self.func

    def decompose(self) -> dict:
        return self.func.to_lists()


def get_output_ta(indicator: IndicatorModel, params: dict, source: ConditionModel):
    """
    Get the technical analysis value of indicator

    Args:
        indicator (IndicatorModel): Indicator object
        params (dict): function parameters
        source (ConditionModel.source): maybe the library for function

    Returns:
        any: maybe technical analysis value
    """
    predefined_indicator = indicator.predefined_indicator
    indicator_id = indicator.to_dict()["id"]

    ta = next((item for item in taS if item["indicator_id"] == indicator_id), None)
    if ta:
        ta = ta["ta"]
        ta.func.add_input_value(params["input_values"])
    else:
        ta = TechnicalAnalysis(predefined_indicator.name, params)
        taS.append({"indicator_id": indicator.to_dict()["id"], "ta": ta})

    # decompose for multiple values output
    try:
        output = ta.decompose()
        output = output[source.source]
    # compose for single value output
    except Exception:
        output = ta.compose()

    return output


def get_params(indicator: IndicatorModel, content: dict) -> dict:
    """
    Get predefined paramters from indicator

    Args:
        indicator (IndicatorModel): indiator object
        content (dict): Callable

    Returns:
        dict: Predifined paramters and the datatype
    """
    params = {}
    params_dao = ParameterModel.get(indicator=indicator)

    for parameter in params_dao:
        # Annotate parameter
        parameter: ParameterModel = parameter
        predifined_params = PredefinedParamModel.get(params=parameter)

        for predifined_param in predifined_params:
            # Annotate predifined-parameter
            predifined_param: PredefinedParamModel = predifined_param
            type = predifined_param.type

            if type == "int":
                value = float(parameter.value)
                params[predifined_param.name] = int(value)
            elif type == "float":
                params[predifined_param.name] = float(parameter.value)
            else:
                params[predifined_param.name] = parameter.value

    # Get input values for params
    if params["input_values"] == "OHLCV":
        ohlcv = OHLCVFactory.from_matrix(
            [
                [
                    content["Open"],  # open
                    content["High"],  # high
                    content["Low"],  # low
                    content["Close"],  # close
                    content["Volume"],  # volume
                ],
            ],
        )
        params["input_values"] = ohlcv
    else:
        params["input_values"] = [content[params["input_values"].title()]]

    return params


if __name__ == "__main__":
    asyncio.run(notification())
