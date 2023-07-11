import json
from pprint import pprint

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from server.utils.indicators import TechnicalAnalysis
from server.utils.ssi.DataClient import DataClient
from server.web.api.indicator.schema import IndicatorDTOModel

router = APIRouter()


@router.get("/")
async def calculate(
    request: Request,
    indicator_dto: IndicatorDTOModel = Depends(),
):
    data_client = DataClient()
    daily_ohlc = data_client.daily_ohlc(
        indicator_dto.symbol,
        indicator_dto.from_date,
        to_date=indicator_dto.to_date,
        page_index=1,
        page_size=100,
    )
    data = daily_ohlc["data"]
    pprint(data)
    ta = TechnicalAnalysis(
        indicator_dto.indicator,
        request.query_params._dict,
    )
    ta.add_input(daily_ohlc)

    return ta.get_outputs()
