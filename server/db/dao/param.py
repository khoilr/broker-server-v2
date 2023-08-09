from server.db.models.indicator import IndicatorModel
from server.db.models.param import ParameterModel
from server.db.models.predefined_param import PredefinedParamModel


class ParamDAO:
    async def create(
        self,
        value: str,
        indicator: IndicatorModel,
        predefined_param: PredefinedParamModel,
    ) -> ParameterModel:
        return await ParameterModel.create(
            value=value,
            indicator=indicator,
            predefined_param=predefined_param,
        )
