from tortoise.transactions import atomic

from server.db.dao.condition import ConditionDAO
from server.db.dao.indicator import IndicatorDAO
from server.db.dao.param import ParamDAO
from server.db.dao.predefined_indicator import PredefinedIndicatorDAO
from server.db.dao.predefined_param import PredefinedParamDAO
from server.db.dao.stock import StockDAO
from server.db.dao.strategy import StrategyDAO
from server.db.dao.telegram import TelegramDAO
from server.db.models.strategy import StrategyModel
from server.db.models.user import UserModel
from server.web.api.indicator.schema import IndicatorInsertionInputDTO
from server.web.api.strategy.schema import StrategyInputDTO

# Define DAOs
predefined_indicator_dao = PredefinedIndicatorDAO()
predefined_param_dao = PredefinedParamDAO()
condition_dao = ConditionDAO()
indicator_dao = IndicatorDAO()
param_dao = ParamDAO()


@atomic()
async def create_strategy(
    user: UserModel,
    strategy_dao: StrategyDAO,
    strategy_dto: StrategyInputDTO,
    stock_dao: StockDAO,
) -> StrategyModel:
    """
    Create strategy object.

    Args:
        user (UserModel): user object
        strategy_dao (StrategyDAO): strategy dao object
        strategy_dto (StrategyInputDTO): strategy dto object
        stock_dao (StockDAO): stock dao obejct

    Returns:
        StrategyModel: strategy object
    """
    # Destructing
    symbols = strategy_dto.symbols
    telegram = strategy_dto.telegram
    indicators = strategy_dto.indicators

    # Get stocks
    stocks = await stock_dao.filter(symbol__in=symbols)

    # Todo: Create a telegram row in database with a username (telegram)
    telegram_dao = TelegramDAO()
    telegram_object = telegram_dao.update_or_create(username=telegram)

    # Todo: Link the telegram to current user (user)
    user.update_or_create(telegram=telegram_object)

    # Create strategy
    strategy = await strategy_dao.create(
        user=user,
        stocks=stocks,
    )

    # Create indicators
    await create_indicator(strategy=strategy, indicators=indicators)

    return strategy


async def create_indicator(
    strategy: StrategyModel,
    indicators: list[IndicatorInsertionInputDTO],
) -> None:
    """
    Create indicator object.

    Args:
        strategy (StrategyModel): strategy object
        indicators (list[IndicatorInsertionInputDTO]): list of indicators input DTO
    """
    # Create indicators
    for indicator in indicators:
        predefined_indicator = await predefined_indicator_dao.get(name=indicator.name)
        new_indicator = await indicator_dao.create(
            strategy=strategy,
            predefined_indicator=predefined_indicator,
        )

        # Create conditions
        condition = indicator.condition
        await condition_dao.create(
            source=condition.source,
            change=condition.change,
            value=condition.value,
            unit=condition.unit,
            indicator=new_indicator,
        )

        # Create params
        for param in indicator.params:
            predefined_param = await predefined_param_dao.get(
                name=param.name,
                predefined_indicator=predefined_indicator,
            )
            await param_dao.create(
                value=param.value,
                indicator=new_indicator,
                predefined_param=predefined_param,
            )
