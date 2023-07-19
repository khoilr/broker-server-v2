from fastapi import APIRouter, Depends, Request

from server.db.dao.predefined_indicator import PredefinedIndicatorDAO
from server.utils.TechnicalAnalysis import TechnicalAnalysis
from server.web.api.indicator.schema import (
    IndicatorCalculationInputDTO,
    IndicatorCalculationOutputDTO,
)
from server.web.api.indicator.util import extract_params, get_price, get_return_data

router = APIRouter()


@router.get(
    "/",
    response_model=IndicatorCalculationOutputDTO,
)
async def calculate(
    request: Request,
    indicator_dto: IndicatorCalculationInputDTO = Depends(),
) -> dict:
    # Get predefined indicator
    predefined_indicator_dao = PredefinedIndicatorDAO()
    predefined_indicator = await predefined_indicator_dao.get(name=indicator_dto.name)

    # Extract parameters
    predefined_params = await predefined_indicator.predefined_params  # type: ignore
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
        name=indicator_dto.name,
        params=params,
    )

    # Add price data
    data = get_price(indicator_dto=indicator_dto)
    data_len = len(data)
    ta.add_inputs(prices=data, input_values=input_values)

    # Get outputs
    try:
        output = ta.decompose()
        data = [
            await get_return_data(k, v, predefined_indicator, data_len)
            for k, v in output.items()
        ]
        response = {
            "same_chart": False,
            "data": data,
            "label": predefined_indicator.label,
            "name": predefined_indicator.name,
        }
    except:
        output = ta.compose()
        output = [0] * (data_len - len(output)) + output
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
