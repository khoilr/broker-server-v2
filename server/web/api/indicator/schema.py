from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class IndicatorInputDTOModel(BaseModel):
    symbol: str
    indicator: str
    from_date: Optional[str] = (datetime.now() - timedelta(days=30)).strftime(
        "%d/%m/%Y",
    )
    to_date: Optional[str] = datetime.now().strftime("%d/%m/%Y")
    orient: Optional[str] = "records"

    class Config:
        orm_mode = False


class DataOutputDTOModel(BaseModel):
    data: list[float]
    name: str
    label: str


class IndicatorOutputDTOModel(BaseModel):
    same_chart: bool
    data: list[DataOutputDTOModel]
