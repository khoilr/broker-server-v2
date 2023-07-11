from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, timedelta
from typing import Union


class IndicatorDTOModel(BaseModel):
    """
    DTO for indicator models.

    It returned when accessing indicator models from the API.
    """

    symbol: str
    indicator: str
    from_date: Optional[str] = (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y")
    to_date: Optional[str] = datetime.now().strftime("%d/%m/%Y")
    orient: Optional[str] = "records"

    class Config:
        orm_mode = False


class IndicatorOutputDTOModel(BaseModel):
    """DTO for indicator models."""

    same_chart: bool
    data: Union[list, dict]


# class IndicatorOutputDTOModel(BaseModel):
#     """
#     DTO for user models.

#     It returned when accessing user models from the API.
#     """


#     class Config:
#         orm_mode = False
