from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel

from server.web.api.condition.schema import ConditionInputDTO
from server.web.api.param.schema import ParamInputDTO


class IndicatorInputDTO(BaseModel):
    name: str


class IndicatorCalculationInputDTO(IndicatorInputDTO):
    symbol: str
    from_date: Optional[str] = (datetime.now() - timedelta(days=30)).strftime(
        "%d/%m/%Y",
    )
    to_date: Optional[str] = datetime.now().strftime("%d/%m/%Y")

    class Config:
        orm_mode = False


class IndicatorInsertionInputDTO(IndicatorInputDTO):
    condition: ConditionInputDTO
    params: list[ParamInputDTO]


class DataOutputDTO(BaseModel):
    data: list[float]
    name: str
    label: str


class IndicatorCalculationOutputDTO(BaseModel):
    same_chart: bool
    data: list[DataOutputDTO]
    name: str
    label: str
