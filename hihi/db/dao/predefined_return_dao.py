from typing import List, Optional

from hihi.db.models.predefined_indicator_model import PredefinedIndicatorModel
from hihi.db.models.predefined_return_model import PredefinedReturnModel


class PredefinedReturnDAO:
    """Class for accessing predefined_return table."""

    async def create(
        self,
        name: str,
        label: str,
        predefined_indicator: PredefinedIndicatorModel,
    ) -> PredefinedReturnModel:
        model = await PredefinedReturnModel.create(
            name=name,
            label=label,
            predefined_indicator=predefined_indicator,
        )
        return model

    async def get(self, name: str, predefined_indicator: PredefinedIndicatorModel) -> PredefinedReturnModel:
        return await PredefinedReturnModel.get(
            name=name,
            predefined_indicator=predefined_indicator,
        )

    async def create_or_get(
        self,
        name: str,
        label: str,
        predefined_indicator: PredefinedIndicatorModel,
    ) -> PredefinedReturnModel:
        return await PredefinedReturnModel.get_or_create(
            name=name,
            label=label,
            predefined_indicator=predefined_indicator,
        )
