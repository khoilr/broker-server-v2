from server.db.models.indicator import IndicatorModel
from server.db.models.predefined_indicator import PredefinedIndicatorModel
from server.db.models.strategy import StrategyModel


class IndicatorDAO:
    """DAO of Indicator model."""

    async def create(
        self,
        strategy: StrategyModel,
        predefined_indicator: PredefinedIndicatorModel,
    ) -> IndicatorModel:
        """
        Create Indicator object using DAO.

        Args:
            strategy (StrategyModel): Strategy object
            predefined_indicator (PredefinedIndicatorModel): Predifined Indicator object

        Returns:
            IndicatorModel: Indicator object
        """
        return await IndicatorModel.create(
            strategy=strategy,
            predefined_indicator=predefined_indicator,
        )
