from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from server.db.dao.strategy import StrategyDAO
from server.db.models.strategy import StrategyModel
from server.db.models.user import UserModel
from server.web.api.strategy.schema import UserDTO, UserModelInputDTO
from utils import auth

router = APIRouter()


@router.post("/")
async def create(
    user: UserModel = Depends(auth.get_current_user),
    strategy_dao: StrategyDAO = Depends(),
):
    return await strategy_dao.create(user=user)


# @router.get("/", response_model=List[StrategyDTO])
# async def get_user_models(
#     limit: int = 10,
#     offset: int = 0,
#     user_dao: UserDAO = Depends(),
# ) -> List[UserModel]:
#     """
#     Retrieve all user objects from the database.

#     :param limit: limit of user objects, defaults to 10.
#     :param offset: offset of user objects, defaults to 0.
#     :param user_dao: DAO for user models.
#     :return: list of user objects from database.
#     """
#     return await user_dao.get_all_users(limit=limit, offset=offset)


# @router.post("/", response_model=UserDTO)
# async def create_user_model(
#     new_user_object: UserModelInputDTO,
#     user_dao: UserDAO = Depends(),
# ) -> UserModel:
#     """
#     Creates user model in the database.

#     :param new_user_object: new user model item.
#     :param user_dao: DAO for user models.
#     """
#     print(new_user_object.dict())
#     return await user_dao.create_user_model(**new_user_object.dict())
