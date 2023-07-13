from typing import List, Optional, Union

from server.db.models.user_model import UserModel


class UserDAO:
    """Class for accessing user table."""

    async def create(self, name: str, username: str, password: str) -> UserModel:
        """
        Add single user to session.

        :param name: name of a user.
        """
        print(name, username, password)

        return await UserModel.create(
            name=name,
            username=username,
            password=password,
        )

    async def get_all(self, limit: int, offset: int) -> List[UserModel]:
        """
        Get all user models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        return await UserModel.all().offset(offset).limit(limit)

    async def filter(self, name: Optional[str] = None) -> List[UserModel]:
        """
        Get specific user model.

        :param name: name of user instance.
        :return: user models.
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

        :param name: name of user instance.
        :return: user models.
        """
        query = UserModel.all()
        if id:
            query = query.filter(id=id).first()
        if username:
            query = query.filter(username=username).first()
        return await query
