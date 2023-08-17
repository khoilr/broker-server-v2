from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from server.db.dao.user import UserDAO
from server.db.models.user import UserModel
from server.web.api.user.schema import UserModelInputDTO, UserOutputDTO

router = APIRouter()


@router.get("/", response_model=List[UserOutputDTO])
async def get_user_models(
    limit: int = 10,
    offset: int = 0,
    user_dao: UserDAO = Depends(),
) -> List[UserModel]:
    """
    Retrieve all user objects from the database.

    Args:
        limit (int): limit of user objects. Defaults to 10.
        offset (int): offset of user objects. Defaults to 0.
        user_dao (UserDAO): DAO for user models. Defaults to Depends().

    Returns:
        List[UserModel]: list of user objects from database.
    """
    return await user_dao.get_all(limit=limit, offset=offset)


@router.post("/", response_model=UserOutputDTO)
async def create_user_model(
    new_user_object: UserModelInputDTO,
    user_dao: UserDAO = Depends(),
) -> UserModel:
    """
    Creates user model in the database.

    Args:
        new_user_object (UserModelInputDTO): new user model item
        user_dao (UserDAO): DAO for user models. Defaults to Depends().

    Returns:
        UserModel: user object
    """
    return await user_dao.create(**new_user_object.dict())
