from functools import partial
from typing import Any

from fastapi import HTTPException
from starlette.datastructures import QueryParams

from server.db.dao.predefined_return import PredefinedReturnDAO
from server.db.models.predefined_indicator import PredefinedIndicatorModel
from server.db.models.predefined_param import PredefinedParamModel
from server.utils.ssi.DataClient import DataClient
from server.web.api.indicator.schema import IndicatorCalculationInputDTO


def extract_params(
    query_params: QueryParams,
    indicator_dto: IndicatorCalculationInputDTO,
    predefined_params: list[PredefinedParamModel],
) -> dict:
    """
    Extract query parameters.

    Args:
        query_params (QueryParams): Query parameters
        indicator_dto (IndicatorCalculationInputDTO): Indicator Calculation Input DTO object
        predefined_params (list[PredefinedParamModel]): List of predifined parameter object

    Raises:
        HTTPException: HTTP error code

    Returns:
        dict: parameters
    """
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


def get_price(indicator_dto: IndicatorCalculationInputDTO) -> list[dict]:
    """
    Get price.

    Args:
        indicator_dto (IndicatorCalculationInputDTO): Indicator Calculation Input DTIO object

    Returns:
        list[dict]: json array or empty array
    """
    data_client = DataClient()
    daily_ohlc = data_client.daily_ohlc(
        symbol=indicator_dto.symbol,
        from_date=indicator_dto.from_date,  # type: ignore
        to_date=indicator_dto.to_date,  # type: ignore
    )
    if daily_ohlc is not None:
        data = daily_ohlc["data"]
        return data
    return []


async def get_return_data(
    k: str,
    v: list[Any],
    predefined_indicator: PredefinedIndicatorModel,
    data_len: int,
) -> dict:
    """
    Get return data.

    Args:
        k (str): Key
        v (list[Any]): Value
        predefined_indicator (PredefinedIndicatorModel): Predifined indicator object
        data_len (int): data length

    Returns:
        dict: data
    """
    predefined_return_dao = PredefinedReturnDAO()
    predefined_return = await predefined_return_dao.get(
        name=k,
        predefined_indicator=predefined_indicator,
    )
    value = [0] * (data_len - len(v)) + v
    return {
        "data": value,
        "name": predefined_return.name,
        "label": predefined_return.label,
    }


if __name__ == "__main__":
    prices = get_price(
        indicator_dto=IndicatorCalculationInputDTO(
            name="BOP",
            symbol="VCB",
            from_date="01/01/2021",
            to_date="30/01/2021",
        ),
    )
