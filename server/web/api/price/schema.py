from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class PriceInputDTO(BaseModel):
    """DTO for price model."""

    symbol: str
    time_frame: Optional[str]
    from_date: Optional[str] = (datetime.now() - timedelta(days=30)).strftime(
        "%d/%m/%Y",
    )
    to_date: Optional[str] = datetime.now().strftime("%d/%m/%Y")
    page_index: Optional[int] = 1
    page_size: Optional[int] = 100

    class Config:
        orm_mode = False
