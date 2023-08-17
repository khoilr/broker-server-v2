from pydantic import BaseModel


class ConditionInputDTO(BaseModel):
    """Input DTO for condition model."""

    source: str
    change: str
    value: float
    unit: str
