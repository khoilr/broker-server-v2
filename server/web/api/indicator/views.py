from functools import partial

from fastapi import APIRouter, Depends, HTTPException, Request

from server.db.dao.predefined_indicator_dao import PredefinedIndicatorDAO
from server.db.dao.predefined_return_dao import PredefinedReturnDAO
from server.db.models.predefined_param_model import PredefinedParamModel
from server.utils.ssi.DataClient import DataClient
from server.utils.TechnicalAnalysis import TechnicalAnalysis
from server.web.api.indicator.schema import (
    IndicatorInputDTOModel,
    IndicatorOutputDTOModel,
)

router = APIRouter()


def extract_params(
    query_params: dict,
    indicator_dto: IndicatorInputDTOModel,
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
        else:
            params[k] = v

        if t:
            try:
                params[k] = t(v)
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid value '{v}' for query parameter '{k}'",
                )
    return params


def get_price(indicator_dto: IndicatorInputDTOModel) -> str:
    data_client = DataClient()
    daily_ohlc = data_client.daily_ohlc(
        symbol=indicator_dto.symbol,
        from_date=indicator_dto.from_date,
        to_date=indicator_dto.to_date,
        page_index=1,
        page_size=100,
    )
    data = daily_ohlc["data"]
    return data


async def get_return_data(k: str, v: list, predefined_indicator):
    predefined_return_dao = PredefinedReturnDAO()
    predefined_return = await predefined_return_dao.get(
        name=k,
        predefined_indicator=predefined_indicator,
    )
    return {
        "data": v,
        "name": predefined_return.name,
        "label": predefined_return.label,
    }


@router.get(
    "/",
    response_model=IndicatorOutputDTOModel,
)
async def calculate(
    request: Request,
    indicator_dto: IndicatorInputDTOModel = Depends(),
) -> dict:
    # Get predefined indicator
    predefined_indicator_dao = PredefinedIndicatorDAO()
    predefined_indicator = await predefined_indicator_dao.get(
        name=indicator_dto.indicator,
    )

    # Extract parameters
    predefined_params = await predefined_indicator.predefined_params
    params = extract_params(
        indicator_dto=indicator_dto,
        predefined_params=predefined_params,
        query_params=request.query_params,
    )

    # Input type
    """Input type should be either OHLCV, Open, High, Low, Close, or Volume"""
    input_values = params.pop("input_values")

    # Init indicator
    ta = TechnicalAnalysis(
        name=indicator_dto.indicator,
        params=params,
    )

    # Add price data
    data = get_price(indicator_dto=indicator_dto)
    ta.add_inputs(prices=data, input_values=input_values)

    # Get outputs
    try:
        output = ta.decompose()
        data = [await get_return_data(k, v, predefined_indicator) for k, v in output.items()]
        response = {
            "same_chart": False,
            "data": data,
            "label": predefined_indicator.label,
            "name": predefined_indicator.name,
        }
    except:
        output = ta.compose()
        response = {
            "same_chart": True,
            "data": [
                {
                    "data": output,
                    "label": predefined_indicator.label,
                    "name": predefined_indicator.name,
                },
            ],
            "name": predefined_indicator.name,
            "label": predefined_indicator.label,
        }

    print(response)

    # Return response
    return response
