from fastapi import APIRouter, Depends

from server.db.dao.stock import StockDAO
from server.db.models.stock import StockModel
from server.web.api.stock.schema import StockOutputDTO

router = APIRouter()


@router.get("/", response_model=list[StockOutputDTO])
async def get_stocks(stock_dao: StockDAO = Depends()) -> list[StockModel]:
    """
    Get stock objects.

    Args:
        stock_dao (StockDAO): stock dao object. Defaults to Depends().

    Returns:
        list[StockModel]: list of stock objects
    """
    return await stock_dao.get_all()
