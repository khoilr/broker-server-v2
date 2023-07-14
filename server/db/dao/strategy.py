from server.db.models.stock import StockModel
from server.db.models.strategy import StrategyModel
from server.db.models.user import UserModel


class StrategyDAO:
    """Class for accessing strategy table."""

    async def create(self, user: UserModel, stocks: list[StockModel]) -> StrategyModel:
        model = await StrategyModel.create(user=user, stocks=stocks)
        return model
