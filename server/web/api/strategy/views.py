from typing import Union

from fastapi import APIRouter, Response
from fastapi.param_functions import Depends
from tortoise.exceptions import OperationalError

from server.db.dao.stock import StockDAO
from server.db.dao.strategy import StrategyDAO
from server.db.models.strategy import StrategyModel
from server.db.models.user import UserModel
from server.utils import auth
from server.web.api.strategy.schema import StrategyInputDTO, StrategyUnrelatedOutputDTO
from server.web.api.strategy.utils import create_strategy

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=StrategyUnrelatedOutputDTO,
)
async def create(
    user: UserModel = Depends(auth.get_current_user),
    strategy_dao: StrategyDAO = Depends(),
    strategy_dto: StrategyInputDTO = Depends(),
    stock_dao: StockDAO = Depends(),
) -> Union[StrategyModel, Response]:
    try:
        strategy = await create_strategy(
            user=user,
            strategy_dao=strategy_dao,
            strategy_dto=strategy_dto,
            stock_dao=stock_dao,
        )
        return strategy
    except OperationalError as e:
        print(e)
        return Response(status_code=422)


@router.get(
    "/",
    response_model=list[StrategyUnrelatedOutputDTO],
)
async def get_all(
    user: UserModel = Depends(auth.get_current_user),
    strategy_dao: StrategyDAO = Depends(),
) -> list[StrategyModel]:
    print(user)
    strategies = await strategy_dao.filter(user=user)
    return strategies
