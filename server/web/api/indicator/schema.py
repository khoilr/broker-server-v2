from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel

from server.web.api.condition.schema import ConditionInputDTO
from server.web.api.param.schema import ParamInputDTO


class IndicatorInputDTO(BaseModel):
    """Input DTO for Indicator model."""

    name: str


class IndicatorCalculationInputDTO(IndicatorInputDTO):
    """Input DTO for Indicator Calculation model."""

    symbol: str
    from_date: Optional[str] = (datetime.now() - timedelta(days=30)).strftime(
        "%d/%m/%Y",
    )
    to_date: Optional[str] = datetime.now().strftime("%d/%m/%Y")

    class Config:
        orm_mode = False


class IndicatorInsertionInputDTO(IndicatorInputDTO):
    """Input DTO for Indicator Insertion model."""

    condition: ConditionInputDTO
    params: list[ParamInputDTO]


class DataOutputDTO(BaseModel):
    """Output DTO for data model."""

    data: list[float]
    name: str
    label: str


class IndicatorCalculationOutputDTO(BaseModel):
    """Output DTO for Indicator Calculation model."""

    same_chart: bool
    data: list[DataOutputDTO]
    name: str
    label: str
