from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, timedelta


class IndicatorDTOModel(BaseModel):
    """
    DTO for user models.

    It returned when accessing user models from the API.
    """

    symbol: str
    indicator: str
    from_date: Optional[str] = (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y")
    to_date: Optional[str] = datetime.now().strftime("%d/%m/%Y")
    orient: Optional[str] = "records"

    class Config:
        orm_mode = False

    # @validator("orient", pre=True, always=True)
    # def set_default_orient(cls, orient):
    #     if orient is None:
    #         return "records"
    #     return orient


# class IndicatorOutputDTOModel(BaseModel):
#     """
#     DTO for user models.

#     It returned when accessing user models from the API.
#     """


#     class Config:
#         orm_mode = False
