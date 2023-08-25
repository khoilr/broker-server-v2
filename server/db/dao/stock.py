from typing import List, Optional

from server.db.models.stock import StockModel


class StockDAO:
    """Class for accessing stock table."""

    async def create(
        self,
        market: str,
        symbol: str,
        name: str,
        en_name: str,
    ) -> StockModel:
        """
        Create Stock object using DAO.

        Args:
            market (str): Market symbol
            symbol (str): Symbol name
            name (str): Full name of stock symbol
            en_name (str): English name

        Returns:
            StockModel: Stock object
        """
        return await StockModel.create(
            market=market,
            symbol=symbol,
            name=name,
            en_name=en_name,
        )

    async def get_by_symbol(self, symbol: Optional[str] = None) -> StockModel:
        """
        Get Stock DAO by symbol.

        Args:
            symbol (str): stock symbol

        Returns:
            StockModel: stock object
        """
        query = StockModel.all()
        if symbol:
            query = query.filter(symbol=symbol).first()
        return await query

    async def get(self, market: Optional[str] = None, symbol: Optional[str] = None) -> StockModel:
        """
        Get Stock object.

        Args:
            market (str): Market symbol
            symbol (str): Symbol name

        Returns:
            StockModel: Stock object
        """
        return await StockModel.get(market=market, symbol=symbol)

    async def get_or_create(
        self,
        market: str,
        symbol: str,
        name: str,
        en_name: str,
    ) -> StockModel:
        """
        Get the stock object, or create it if none exists.

        Args:
            market (str): Market symbol
            symbol (str): Symbol name
            name (str): Full name of stock symbol
            en_name (str): English name

        Returns:
            StockModel: Stock object
        """
        return await StockModel.get_or_create(
            market=market,
            symbol=symbol,
            name=name,
            en_name=en_name,
        )

    async def filter(
        self,
        **kwargs,
    ) -> List[StockModel]:
        """
        Filter the stock symbol.

        Returns:
            **kwargs: filter criteria
            List[StockModel]: list of stock objects
        """
        return await StockModel.filter(**kwargs)

    async def update(
        self,
        market: str,
        symbol: str,
        name: str,
        en_name: str,
    ) -> StockModel:
        """
        Update stock object.

        Args:
            market (str): Market symbol
            symbol (str): Symbol name
            name (str): Full name of the stock
            en_name (str): English name

        Returns:
            StockModel: Stock object
        """
        model = await StockModel.get(market=market, symbol=symbol)
        model.name = name
        model.en_name = en_name
        await model.save()
        return model

    async def delete(self, market: str, symbol: str) -> None:
        """
        Delete stock object.

        Args:
            market (str): Market symbol
            symbol (str): Symbol name
        """
        await StockModel.filter(market=market, symbol=symbol).delete()

    async def get_all(self) -> List[StockModel]:
        """
        Get all the stock objects.

        Returns:
            List[StockModel]: List of stock objects
        """
        return await StockModel.all()
