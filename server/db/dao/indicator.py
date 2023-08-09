from server.db.models.indicator import IndicatorModel
from server.db.models.predefined_indicator import PredefinedIndicatorModel
from server.db.models.strategy import StrategyModel


class IndicatorDAO:
    async def create(
        self,
        strategy: StrategyModel,
        predefined_indicator: PredefinedIndicatorModel,
    ) -> IndicatorModel:
        return await IndicatorModel.create(
            strategy=strategy,
            predefined_indicator=predefined_indicator,
        )
