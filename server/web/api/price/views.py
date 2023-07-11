from fastapi import APIRouter, Depends
from server.utils.ssi.DataClient import DataClient
from server.web.api.price.schema import PriceInputModelDTO

router = APIRouter()


@router.get("/daily")
async def get_daily_price(price_model_dto: PriceInputModelDTO = Depends()):
    data_client = DataClient()
    return data_client.daily_ohlc(
        symbol=price_model_dto.symbol,
        from_date=price_model_dto.from_date,
        to_date=price_model_dto.to_date,
        page_index=price_model_dto.page_index,
        page_size=price_model_dto.page_size,
    )["data"]
