from typing import List

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
        return await StockModel.create(
            market=market,
            symbol=symbol,
            name=name,
            en_name=en_name,
        )

    async def get(self, market: str, symbol: str) -> StockModel:
        return await StockModel.get(market=market, symbol=symbol)

    async def get_by_name(self,symbol: str) -> StockModel:
        return await StockModel.get(symbol=symbol)

    async def get_or_create(
        self,
        market: str,
        symbol: str,
        name: str,
        en_name: str,
    ) -> StockModel:
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
        return await StockModel.filter(**kwargs)

    async def update(
        self,
        market: str,
        symbol: str,
        name: str,
        en_name: str,
    ) -> StockModel:
        model = await StockModel.get(market=market, symbol=symbol)
        model.name = name
        model.en_name = en_name
        await model.save()
        return model

    async def delete(self, market: str, symbol: str) -> None:
        await StockModel.filter(market=market, symbol=symbol).delete()

    async def get_all(self) -> List[StockModel]:
        return await StockModel.all()
