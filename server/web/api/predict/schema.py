from pydantic import BaseModel


class PredictOutputDTO(BaseModel):
    symbol: str
    probability: float

class PredictInputDTO(BaseModel):
    symbol: str
