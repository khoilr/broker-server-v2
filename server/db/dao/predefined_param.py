from server.db.models.predefined_indicator import PredefinedIndicatorModel
from server.db.models.predefined_param import PredefinedParamModel


class PredefinedParamDAO:
    """Class for accessing predefined_param table."""

    async def get_or_create(
        self,
        name: str,
        label: str,
        predefined_indicator: PredefinedIndicatorModel,
        _type: str,
    ) -> PredefinedParamModel:
        """
        Get Predefined Parameter object, or create if no object exists.

        Args:
            name (str): name of Predifined Parameter
            label (str): label of Predifined Parameter
            predefined_indicator (PredefinedIndicatorModel): Predefined Indicator object
            _type (str): type

        Returns:
            PredefinedParamModel: Predefined Param object
        """
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
        """
        Create Predifinded Parameter object using DAO.

        Args:
            name (str): name of Predifined Parameter
            label (str): label of Predifined Parameter
            predefined_indicator (PredefinedIndicatorModel): Predefined Indicator object
            type (str): type

        Returns:
            PredefinedParamModel: Predefined Param object
        """
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
        """
        Get Predifinded Parameter object using DAO.

        Args:
            name (str): name of Predifined Parameter
            predefined_indicator (PredefinedIndicatorModel): Predefined Indicator object

        Returns:
            PredefinedParamModel: Predefined Param object
        """
        return await PredefinedParamModel.get(
            name=name,
            predefined_indicator=predefined_indicator,
        )
