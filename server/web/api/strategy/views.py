from typing import Union

from fastapi import APIRouter, Response
from fastapi.param_functions import Depends

from server.db.dao.stock import StockDAO
from server.db.dao.strategy import StrategyDAO
from server.db.models.strategy import StrategyModel
from server.db.models.user import UserModel
from server.utils import auth
from server.web.api.strategy.schema import StrategyInputDTO, StrategyUnrelatedOutputDTO
from server.web.api.strategy.util import create_strategy

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=StrategyUnrelatedOutputDTO,
)
async def create(
    strategy_dto: StrategyInputDTO,
    user: UserModel = Depends(auth.get_current_user),
    strategy_dao: StrategyDAO = Depends(),
    stock_dao: StockDAO = Depends(),
) -> Union[StrategyModel, Response]:
    """
    Create strategy object.

    Args:
        user (UserModel): user object. Defaults to Depends(auth.get_current_user).
        strategy_dao (StrategyDAO): strategy dao. Defaults to Depends().
        strategy_dto (StrategyInputDTO): strategy dto. Defaults to Depends().
        stock_dao (StockDAO): stock dao. Defaults to Depends().

    Returns:
        Union[StrategyModel, Response]: Union object
    """
    # try:
    strategy = await create_strategy(
        user=user,
        strategy_dao=strategy_dao,
        strategy_dto=strategy_dto,
        stock_dao=stock_dao,
    )
    return strategy
    # except OperationalError:
    # return Response(status_code=422)


@router.get(
    "/",
    response_model=list[StrategyUnrelatedOutputDTO],
)
async def get_all(
    user: UserModel = Depends(auth.get_current_user),
    strategy_dao: StrategyDAO = Depends(),
) -> list[StrategyModel]:
    """
    Get all strategy objects.

    Args:
        user (UserModel): user object. Defaults to Depends(auth.get_current_user).
        strategy_dao (StrategyDAO): strategy dao object. Defaults to Depends().

    Returns:
        list[StrategyModel]: lists of strategy objects
    """
    strategies = await strategy_dao.filter(user=user)
    return strategies
