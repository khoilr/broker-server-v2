from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from server.db.dao.user_dao import UserDAO
from server.db.models.user_model import UserModel
from server.web.api.user.schema import UserModelInputDTO, UserOutputModelDTO

router = APIRouter()


@router.get("/", response_model=List[UserOutputModelDTO])
async def get_user_models(
    limit: int = 10,
    offset: int = 0,
    user_dao: UserDAO = Depends(),
) -> List[UserModel]:
    """
    Retrieve all user objects from the database.

    :param limit: limit of user objects, defaults to 10.
    :param offset: offset of user objects, defaults to 0.
    :param user_dao: DAO for user models.
    :return: list of user objects from database.
    """
    return await user_dao.get_all(limit=limit, offset=offset)


@router.post("/", response_model=UserOutputModelDTO)
async def create_user_model(
    new_user_object: UserModelInputDTO,
    user_dao: UserDAO = Depends(),
) -> UserModel:
    """
    Creates user model in the database.

    :param new_user_object: new user model item.
    :param user_dao: DAO for user models.
    """
    print(new_user_object.dict())
    return await user_dao.create(**new_user_object.dict())
