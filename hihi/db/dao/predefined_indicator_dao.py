from typing import List, Optional
from hihi.db.models.predefined_indicator_model import PredefinedIndicatorModel


class PredefinedIndicatorDAO:
    """Class for accessing predefined_indicator table."""

    async def create(self, name: str, label: str) -> PredefinedIndicatorModel:
        return await PredefinedIndicatorModel.create(name=name, label=label)

    async def get(self, name: str) -> PredefinedIndicatorModel:
        return await PredefinedIndicatorModel.get(name=name)

    async def get_or_create(self, name: str, label: str) -> PredefinedIndicatorModel:
        return await PredefinedIndicatorModel.get_or_create(
            name=name,
            label=label,
        )
