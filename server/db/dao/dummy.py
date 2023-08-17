from typing import List, Optional

from server.db.models.dummy import DummyModel


class DummyDAO:
    """Class for accessing dummy table."""

    async def create_dummy_model(self, name: str) -> DummyModel:
        """
        Create dummy object.

        Args:
            name (str): dummy object name

        Returns:
            DummyModel: Dummy object
        """
        return await DummyModel.create(name=name)

    async def get_all_dummies(self, limit: int, offset: int) -> List[DummyModel]:
        """
        Get all dummy objects.

        Args:
            limit (int): number
            offset (int): query offset

        Returns:
            List[DummyModel]: list of dummy objects
        """
        return await DummyModel.all().offset(offset).limit(limit)

    async def filter(self, name: Optional[str] = None) -> List[DummyModel]:
        """
        Get specific dummy object.

        Args:
            name (Optional[str], optional): name of dummy instance. Defaults to None.

        Returns:
            List[DummyModel]: dummy objects.
        """
        query = DummyModel.all()
        if name:
            query = query.filter(name=name)
        return await query
