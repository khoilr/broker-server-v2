from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, timedelta
from typing import Union


class IndicatorInputDTOModel(BaseModel):
    symbol: str
    indicator: str
    from_date: Optional[str] = (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y")
    to_date: Optional[str] = datetime.now().strftime("%d/%m/%Y")
    orient: Optional[str] = "records"

    class Config:
        orm_mode = False


class IndicatorOutputDTOModel(BaseModel):
    same_chart: bool
    data: Union[list, dict]
