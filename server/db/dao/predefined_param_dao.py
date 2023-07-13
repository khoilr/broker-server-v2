from server.db.models.predefined_indicator_model import PredefinedIndicatorModel
from server.db.models.predefined_param_model import PredefinedParamModel


class PredefinedParamDAO:
    """Class for accessing predefined_param table."""

    async def get_or_create(
        self,
        name: str,
        label: str,
        predefined_indicator: PredefinedIndicatorModel,
        _type: str,
    ) -> PredefinedParamModel:
        return await PredefinedParamModel.get_or_create(
            name=name,
            label=label,
            predefined_indicator=predefined_indicator,
            type=_type,
        )

    async def create(
        self,
        name: str,
        label: str,
        predefined_indicator: PredefinedIndicatorModel,
        type: str,
    ) -> PredefinedParamModel:
        return await PredefinedParamModel.create(
            name=name,
            label=label,
            predefined_indicator=predefined_indicator,
            type=type,
        )

    async def get(
        self,
        name: str,
        predefined_indicator: PredefinedIndicatorModel,
    ) -> PredefinedParamModel:
        return await PredefinedParamModel.get(
            name=name,
            predefined_indicator=predefined_indicator,
        )
