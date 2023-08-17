from datetime import datetime

from pydantic import BaseModel


class StockOutputDTO(BaseModel):
    """Output DTO for stock model."""

    id: int
    market: str
    name: str
    updated_at: datetime
    created_at: datetime
    en_name: str
    symbol: str
