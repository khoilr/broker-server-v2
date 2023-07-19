import asyncio
import json
import time

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from talipp.ohlcv import OHLCVFactory

from server.utils.ssi.DataStream import MarketDataStream

taS = []

telegram_bot = None


async def notification(bot):
    # Init bot
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))  # type: ignore
    storage = MemoryStorage()

    selected_channel = "B:ALL"
    data_stream = MarketDataStream(
        on_message=on_message,
        on_error=on_error,
    )
    data_stream.start(selected_channel)


async def notify(strategy, notification_string: str):
    user = strategy.user

    # Telegram
    if user.telegram_account is not None:
        telegram_account = user.telegram_account

        # When telegram user is registered
        if telegram_account.id is not None:
            # Manual commit
            # This is to prevent the database from being locked
            # Send message to telegram
            await telegram_bot.send_message(
                chat_id=user.telegram_account.id,
                text=notification_string,
            )
            # Modify notified to True
            # notified_strategy["notified"] = True
    else:
        # # Modify notified to False in the list if condition is not met
        # notified_strategy["notified"] = False
        pass


def on_message(message):
    global taS

    try:
        # Get symbol from message
        content = json.loads(message["Content"])
        symbol = content["Symbol"]

        # Interrupt if symbol is not in redis
        if not redis_db.exists(symbol):
            return

        # get key is symbol, the value is a list of dict [{id: 1, active: False}]. Filter by id
        notified_strategies = redis_db.lrange(symbol, 0, -1)

        with db_session:
            # Get strategies from database
            strategies = Strategy.select(stock=symbol)

            # print(content)

            # For each strategy
            for strategy in strategies:
                is_met_condition = True
                notification_string = ""

                # For each indicator
                for indicator in strategy.indicators:
                    # Get parameters for indicator
                    params = get_params(indicator=indicator, content=content)

                    # Get condition
                    condition = indicator.condition

                    # Get technical analysis
                    output = get_output_ta(
                        indicator=indicator,
                        params=params,
                        source=condition.source,
                    )

                    # print(output)

                    # Check if condition is met
                    is_met_condition = is_meet_condition(
                        output=output,
                        condition=condition,
                    )

                    # Concat notification string
                    if is_met_condition:
                        notification_string += f"{indicator.indicator_ta.name} {condition.change} {condition.value}\n"
                    else:
                        for notified_strategy in notified_strategies:
                            # parse notified_strategy to dict
                            notified_strategy_dict = json.loads(notified_strategy)

                            # If strategy is not notified
                            if notified_strategy_dict["id"] == strategy.id and notified_strategy_dict["active"]:
                                # Modify notified to True
                                notified_strategy_dict["active"] = False

                                # Modify the list in redis
                                redis_db.lset(
                                    symbol,
                                    notified_strategies.index(notified_strategy),
                                    json.dumps(notified_strategy_dict),
                                )

                                break

                if is_met_condition:
                    # notified_strategy and notified_strategy_index
                    for notified_strategy in notified_strategies:
                        # parse notified_strategy to dict
                        notified_strategy_dict = json.loads(notified_strategy)

                        # If strategy is not notified
                        if notified_strategy_dict["id"] == strategy.id and not notified_strategy_dict["active"]:
                            # Modify notified to True
                            notified_strategy_dict["active"] = False

                            # Modify the list in redis
                            redis_db.lset(
                                symbol, notified_strategies.index(notified_strategy), json.dumps(notified_strategy_dict)
                            )

                            # Run notify asynchronously
                            asyncio.run(
                                notify(
                                    strategy=strategy,
                                    notification_string=notification_string,
                                )
                            )

                            break

    except Exception as e:
        print(e)


def get_params(indicator: Indicator, content: dict) -> dict:
    params = {}
    for parameter in indicator.parameters:
        parameter_ta = parameter.parameter_ta

        if parameter_ta.type == "int":
            value = float(parameter.value)
            params[parameter_ta.name] = int(value)
        elif parameter_ta.type == "float":
            params[parameter_ta.name] = float(parameter.value)
        else:
            params[parameter_ta.name] = parameter.value

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
                ]
            ]
        )
        params["input_values"] = ohlcv
    else:
        params["input_values"] = [content[params["input_values"].title()]]

    return params


def get_output_ta(indicator, params, source):
    indicator_ta = indicator.indicator_ta
    indicator_id = indicator.to_dict()["id"]

    ta = next((item for item in taS if item["indicator_id"] == indicator_id), None)
    if ta:
        ta = ta["ta"]
        ta.func.add_input_value(params["input_values"])
    else:
        ta = TechnicalAnalysis(indicator_ta.name, params)
        taS.append({"indicator_id": indicator.to_dict()["id"], "ta": ta})

    # decompose for multiple values output
    try:
        output = ta.decompose()
        output = output[source]
    # compose for single value output
    except:
        output = ta.compose()

    return output


def is_meet_condition(output, condition) -> bool:
    if len(output) > 0:
        return True if eval(f"{output[-1]} {condition.change} {condition.value}") else False
    else:
        return False


def on_error(error):
    print(error)
