from typing import List

from server.db.models.predefined_indicator import PredefinedIndicatorModel


class PredefinedIndicatorDAO:
    """Class for accessing predefined_indicator table."""

    async def create(self, name: str, label: str) -> PredefinedIndicatorModel:
        return await PredefinedIndicatorModel.create(name=name, label=label)

    async def get(self, name: str) -> PredefinedIndicatorModel:
        return await PredefinedIndicatorModel.get(name=name)

    async def get_or_create(
        self, name: str, label: str
    ) -> tuple[PredefinedIndicatorModel, bool]:
        return await PredefinedIndicatorModel.get_or_create(
            name=name,
            label=label,
        )

    async def get_all(self) -> List[PredefinedIndicatorModel]:
        return await PredefinedIndicatorModel.all().prefetch_related(
            "predefined_params",
            "predefined_returns",
        )
