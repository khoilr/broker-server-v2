from datetime import datetime

from pydantic import BaseModel

from server.web.api.indicator.schema import IndicatorInsertionInputDTO


class StrategyInputDTO(BaseModel):
    """Input DTO for strategy-unrelated object."""

    symbols: list[str]
    telegram: str
    indicators: list[IndicatorInsertionInputDTO] = []

    class Config:
        orm_mode = True


class StrategyUnrelatedOutputDTO(BaseModel):
    """Output DTO for strategy-unrelated object."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
