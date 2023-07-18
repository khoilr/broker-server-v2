from pydantic import BaseModel


class ConditionInputDTO(BaseModel):
    source: str
    change: str
    value: float
    unit: str
