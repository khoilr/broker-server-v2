from server.db.models.predefined_indicator import PredefinedIndicatorModel
from server.db.models.predefined_return import PredefinedReturnModel


class PredefinedReturnDAO:
    """Class for accessing predefined_return table."""

    async def create(
        self,
        name: str,
        label: str,
        predefined_indicator: PredefinedIndicatorModel,
    ) -> PredefinedReturnModel:
        """
        Create Predifined Return object.

        Args:
            name (str): name of Predifined Return object
            label (str): label of Predifined Return object
            predefined_indicator (PredefinedIndicatorModel): Predifined Indicator object

        Returns:
            PredefinedReturnModel: Predifined Return object
        """
        model = await PredefinedReturnModel.create(
            name=name,
            label=label,
            predefined_indicator=predefined_indicator,
        )
        return model

    async def get(
        self,
        name: str,
        predefined_indicator: PredefinedIndicatorModel,
    ) -> PredefinedReturnModel:
        """
        Get Predifined Return object.

        Args:
            name (str): name of Predifined Return object
            predefined_indicator (PredefinedIndicatorModel): Predifined Indicator object

        Returns:
            PredefinedReturnModel: Predifined Return object
        """
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
        """
        Get Predifined Return object, or create if no object exists.

        Args:
            name (str): name of Predifined Return object
            label (str): label of Predifined Return object
            predefined_indicator (PredefinedIndicatorModel): Predifined Indicator object

        Returns:
            PredefinedReturnModel: Predifined Return object
        """
        return await PredefinedReturnModel.get_or_create(
            name=name,
            label=label,
            predefined_indicator=predefined_indicator,
        )
