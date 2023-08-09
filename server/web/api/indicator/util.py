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
    data_client = DataClient()
    daily_ohlc = data_client.daily_ohlc(
        symbol=indicator_dto.symbol,
        from_date=indicator_dto.from_date,  # type: ignore
        to_date=indicator_dto.to_date,  # type: ignore
    )
    if daily_ohlc is not None:
        data = daily_ohlc["data"]
        return data
    else:
        return []


async def get_return_data(
    k: str,
    v: list[Any],
    predefined_indicator: PredefinedIndicatorModel,
    data_len: int,
):
    predefined_return_dao = PredefinedReturnDAO()
    predefined_return = await predefined_return_dao.get(
        name=k,
        predefined_indicator=predefined_indicator,
    )
    v = [0] * (data_len - len(v)) + v
    return {
        "data": v,
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
    print(prices)
