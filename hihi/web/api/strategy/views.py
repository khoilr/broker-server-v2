# from typing import List

# from fastapi import APIRouter
# from fastapi.param_functions import Depends

# from hihi.db.dao.strategy_dao import StrategyDAO
# from hihi.db.models.strategy_model import StrategyModel
# from hihi.web.api.strategy.schema import UserModelDTO, UserModelInputDTO

# router = APIRouter()


# @router.get("/", response_model=List[StrategyModelDTO])
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


# @router.post("/", response_model=UserModelDTO)
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
