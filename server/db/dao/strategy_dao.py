from server.db.models.strategy_model import StrategyModel
from server.db.models.user_model import UserModel
from server.db.models.stock_model import StockModel


class StrategyDAO:
    """Class for accessing strategy table."""

    async def create(self, user: UserModel, stock: StockModel) -> StrategyModel:
        model = await StrategyModel.create(
            user=user,
            stock=stock,
        )
        return model
