from server.db.models.stock import StockModel
from server.db.models.strategy import StrategyModel
from server.db.models.user import UserModel


class StrategyDAO:
    async def create(self, user: UserModel, stocks: list[StockModel]) -> StrategyModel:
        strategy = await StrategyModel.create(user=user)
        await strategy.stocks.add(*stocks)
        return strategy

    async def filter(self, user: UserModel) -> list[StrategyModel]:
        return await StrategyModel.filter(user=user)
