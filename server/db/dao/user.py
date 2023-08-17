from typing import List, Optional, Union

from server.db.models.user import UserModel


class UserDAO:
    """Class for accessing user table."""

    async def create(self, name: str, username: str, password: str) -> UserModel:
        """
        Add single user to session.

        Args:
            name (str): Name of a user
            username (str): username
            password (str): user password

        Returns:
            UserModel: User object
        """
        return await UserModel.create(
            name=name,
            username=username,
            password=password,
        )

    async def get_all(self, limit: int, offset: int) -> List[UserModel]:
        """
        Get all user models with limit/offset pagination.

        Args:
            limit (int): limit of dummies.
            offset (int): offset of dummies.

        Returns:
            List[UserModel]: stream of dummies.
        """
        return await UserModel.all().offset(offset).limit(limit)

    async def filter(self, name: Optional[str] = None) -> List[UserModel]:
        """
        Get specific user model.

        Args:
            name (Optional[str], optional): name of user instance.. Defaults to None.

        Returns:
            List[UserModel]: user models.
        """
        query = UserModel.all()
        if name:
            query = query.filter(name=name)
        return await query

    async def get(
        self,
        id: Optional[int] = None,
        username: Optional[str] = None,
    ) -> Union[UserModel, None]:
        """
        Get specific user model.

        Args:
            id (Optional[int], optional): User id. Defaults to None.
            username (Optional[str], optional): Username. Defaults to None.

        Returns:
            Union[UserModel, None]: User object, return None if none exists
        """
        query = UserModel.all()
        if id:
            query = query.filter(id=id).first()
        elif username:
            query = query.filter(username=username).first()
        else:
            return None
        return await query
