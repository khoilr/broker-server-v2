from pydantic import BaseModel


class StrategyModelDTO(BaseModel):
    """
    DTO for user models.

    It returned when accessing user models from the API.
    """

    id: int
    name: str

    class Config:
        orm_mode = True


class StrategyModelInputDTO(BaseModel):
    """DTO for creating new user model."""

    name: str
