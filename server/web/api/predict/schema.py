from pydantic import BaseModel


class PredictOutputDTO(BaseModel):
    symbol: str
    probability_day: float
    probability_week: float


class PredictInputDTO(BaseModel):
    symbol: str
