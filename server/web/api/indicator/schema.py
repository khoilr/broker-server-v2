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
    from_date: str
    to_date: str
    orient: Optional[str]

    class Config:
        orm_mode = False

    @validator("orient", pre=True, always=True)
    def set_default_orient(cls, orient):
        if orient is None:
            return "records"
        return orient


# class IndicatorOutputDTOModel(BaseModel):
#     """
#     DTO for user models.

#     It returned when accessing user models from the API.
#     """


#     class Config:
#         orm_mode = False
