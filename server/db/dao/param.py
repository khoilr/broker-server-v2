from server.db.models.indicator import IndicatorModel
from server.db.models.param import ParameterModel
from server.db.models.predefined_param import PredefinedParamModel


class ParamDAO:
    """DAO of Parameter model."""

    async def create(
        self,
        value: str,
        indicator: IndicatorModel,
        predefined_param: PredefinedParamModel,
    ) -> ParameterModel:
        """
        Create Parameter object using DAO.

        Args:
            value (str): Value
            indicator (IndicatorModel): Indicator object
            predefined_param (PredefinedParamModel): Predifined Parameter object

        Returns:
            ParameterModel: Parameter object
        """
        return await ParameterModel.create(
            value=value,
            indicator=indicator,
            predefined_param=predefined_param,
        )
