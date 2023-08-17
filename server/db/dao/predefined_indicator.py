from typing import List

from server.db.models.predefined_indicator import PredefinedIndicatorModel


class PredefinedIndicatorDAO:
    """Class for accessing predefined_indicator table."""

    async def create(self, name: str, label: str) -> PredefinedIndicatorModel:
        """
        Create Predifined Indicator model using DAO.

        Args:
            name (str): name of predifined indicator
            label (str): label of predifined indicator

        Returns:
            PredefinedIndicatorModel: Predifined Indicator object
        """
        return await PredefinedIndicatorModel.create(name=name, label=label)

    async def get(self, name: str) -> PredefinedIndicatorModel:
        """
        Get Predifined Indicator object using DAO.

        Args:
            name (str): name of predifined indicator

        Returns:
            PredefinedIndicatorModel: Predifined Indicator object
        """
        return await PredefinedIndicatorModel.get(name=name)

    async def get_or_create(
        self,
        name: str,
        label: str,
    ) -> tuple[PredefinedIndicatorModel, bool]:
        """
        Get or create.

        Args:
            name (str): name of predifined indicator
            label (str): label of predifined indicator

        Returns:
            tuple[PredefinedIndicatorModel, bool]: Predifined Indicator object,
            and True if the object already exists, False if the new object is created
        """
        return await PredefinedIndicatorModel.get_or_create(
            name=name,
            label=label,
        )

    async def get_all(self) -> List[PredefinedIndicatorModel]:
        """
        Get all the Predifined Indicator objects.

        Returns:
            List[PredefinedIndicatorModel]: list of Predifined Indicator objects
        """
        return await PredefinedIndicatorModel.all().prefetch_related(
            "predefined_params",
            "predefined_returns",
        )
