from server.db.models.condition import ConditionModel
from server.db.models.indicator import IndicatorModel


class ConditionDAO:
    """DAO of condition model."""

    async def create(
        self,
        source: str,
        change: str,
        value: float,
        unit: str,
        indicator: IndicatorModel,
    ) -> ConditionModel:
        """
        Create a new condition object using DAO.

        Args:
            source (str): Talipp source
            change (str): type of change
            value (float): value
            unit (str): unit
            indicator (IndicatorModel): indicator object

        Returns:
            ConditionModel: Condition object
        """
        return await ConditionModel.create(
            source=source,
            change=change,
            value=value,
            unit=unit,
            indicator=indicator,
        )
