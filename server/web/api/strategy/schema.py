from datetime import datetime

from pydantic import BaseModel

from server.web.api.indicator.schema import IndicatorInsertionInputDTO


class StrategyInputDTO(BaseModel):
    symbols: list[str]
    indicators: list[IndicatorInsertionInputDTO] = []

    class Config:
        orm_mode = True


class StrategyUnrelatedOutputDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
