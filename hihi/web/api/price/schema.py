from datetime import datetime, timedelta
from pydantic import BaseModel, validator
from typing import Optional


class PriceModelDTO(BaseModel):
    symbol: str
    time_frame: Optional[str]
    from_date: Optional[str]
    to_date: Optional[str]
    page_index: Optional[int]
    page_size: Optional[int]

    class Config:
        orm_mode = False

    @validator("from_date", pre=True, always=True)
    def set_default_from_date(cls, from_date, values):
        if not from_date:
            default_from_date = (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y")
            return default_from_date
        return from_date

    @validator("to_date", pre=True, always=True)
    def set_default_to_date(cls, to_date, values):
        if not to_date:
            default_to_date = datetime.now().strftime("%d/%m/%Y")
            return default_to_date
        return to_date

    @validator("page_index", pre=True, always=True)
    def set_default_page_index(cls, page_index, values):
        if page_index is None:
            return 1
        return page_index

    @validator("page_size", pre=True, always=True)
    def set_default_page_size(cls, page_size, values):
        if page_size is None:
            return 100
        return page_size
