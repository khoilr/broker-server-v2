from fastapi import APIRouter, Depends

from server.utils.ssi.DataClient import DataClient
from server.web.api.price.schema import PriceInputDTO

router = APIRouter()


@router.get("/daily")
async def get_daily_price(price_model_dto: PriceInputDTO = Depends()):
    data_client = DataClient()
    return data_client.daily_ohlc(
        symbol=price_model_dto.symbol,
        from_date=price_model_dto.from_date,  # type: ignore
        to_date=price_model_dto.to_date,  # type: ignore
    )["data"]
