from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class IndicatorInputDTO(BaseModel):
    symbol: str
    indicator: str
    from_date: Optional[str] = (datetime.now() - timedelta(days=30)).strftime(
        "%d/%m/%Y",
    )
    to_date: Optional[str] = datetime.now().strftime("%d/%m/%Y")
    orient: Optional[str] = "records"

    class Config:
        orm_mode = False


class DataOutputDTO(BaseModel):
    data: list[float]
    name: str
    label: str


class IndicatorOutputDTO(BaseModel):
    same_chart: bool
    data: list[DataOutputDTO]
    name: str
    label: str
