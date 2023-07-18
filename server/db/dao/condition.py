from server.db.models.condition import ConditionModel
from server.db.models.indicator import IndicatorModel


class ConditionDAO:
    async def create(
        self,
        source: str,
        change: str,
        value: float,
        unit: str,
        indicator: IndicatorModel,
    ) -> ConditionModel:
        return await ConditionModel.create(
            source=source,
            change=change,
            value=value,
            unit=unit,
            indicator=indicator,
        )
