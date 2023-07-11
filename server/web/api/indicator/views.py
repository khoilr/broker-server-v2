from functools import partial
import json
from pprint import pprint
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from server.utils.indicators import TechnicalAnalysis
from server.utils.ssi.DataClient import DataClient
from server.web.api.indicator.schema import IndicatorDTOModel
from server.db.dao.predefined_indicator_dao import PredefinedIndicatorDAO
from server.db.models.predefined_param_model import PredefinedParamModel


router = APIRouter()


def extract_params(
    query_params: dict,
    indicator_dto: IndicatorDTOModel,
    predefined_params: list[PredefinedParamModel],
) -> dict:
    params = {}
    for k, v in query_params.items():
        if k in indicator_dto.dict():
            continue

        predefined_param = next(filter(lambda x: x.name == k, predefined_params), None)
        if not predefined_param:
            continue

        t = None
        if predefined_param.type == "str":
            t = str
        elif predefined_param.type == "int":
            t = partial(int, base=10)
        elif predefined_param.type == "float":
            t = float
        elif predefined_param.type == "bool":
            t = lambda x: x.lower() in ["true", "1", "yes"]

        if t:
            try:
                params[k] = t(v)
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid value '{v}' for query parameter '{k}'",
                )
    return params


@router.get("/")
async def calculate(
    request: Request,
    indicator_dto: IndicatorDTOModel = Depends(),
):
    # Get daily ohlc
    data_client = DataClient()
    daily_ohlc = data_client.daily_ohlc(
        indicator_dto.symbol,
        indicator_dto.from_date,
        to_date=indicator_dto.to_date,
        page_index=1,
        page_size=100,
    )
    data = daily_ohlc["data"]

    # Get predefined indicator
    predefined_indicator_dao = PredefinedIndicatorDAO()
    predefined_indicator = await predefined_indicator_dao.get(name=indicator_dto.indicator.upper())

    # Extract parameters
    predefined_params = await predefined_indicator.predefined_params
    params = extract_params(
        indicator_dto=indicator_dto,
        predefined_params=predefined_params,
        query_params=request.query_params,
    )

    # Calculate indicator
    ta = TechnicalAnalysis(
        name=indicator_dto.indicator.upper(),
        kwargs=params,
    )
    ta.add_inputs(prices=data, input_type="close")

    # Get outputs
    try:
        output = ta.decompose()
        print("decompose")
        print(output)
        response = {
            "same_chart": False,
            "data": output,
        }
    except:
        output = ta.compose()
        print("compose")
        print(output)
        print(type(output))
        response = {
            "same_chart": True,
            "data": output,
        }

    # Return response
    return response
