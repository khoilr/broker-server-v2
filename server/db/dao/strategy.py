from server.db.models.stock import StockModel
from server.db.models.strategy import StrategyModel
from server.db.models.user import UserModel


class StrategyDAO:
    """Class for accessing Strategy table."""

    async def create(self, user: UserModel, stocks: list[StockModel]) -> StrategyModel:
        """
        Create a new Strategy object using DAO.

        Args:
            user (UserModel): User object
            stocks (list[StockModel]): List of stock objects

        Returns:
            StrategyModel: Strategy object
        """
        strategy = await StrategyModel.create(user=user)
        await strategy.stocks.add(*stocks)
        return strategy

    async def filter(self, user: UserModel) -> list[StrategyModel]:
        """
        Filter strategy objects based on user object.

        Args:
            user (UserModel): user object

        Returns:
            list[StrategyModel]: list of strategy objects of given user
        """
        return await StrategyModel.filter(user=user)

    async def filter_from_stock(self, stock: StockModel) -> list[StrategyModel]:
        """
        Filter strategy objects based on user object.

        Args:
            user (UserModel): user object

        Returns:
            list[StrategyModel]: list of strategy objects of given user
        """
        return await StrategyModel.filter(
            stocks=[stock],
        )
