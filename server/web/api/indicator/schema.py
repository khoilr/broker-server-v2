from pydantic import BaseModel
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
    orient: str

    class Config:
        orm_mode = False


# class IndicatorOutputDTOModel(BaseModel):
#     """
#     DTO for user models.

#     It returned when accessing user models from the API.
#     """


#     class Config:
#         orm_mode = False
