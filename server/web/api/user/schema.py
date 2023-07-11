from pydantic import BaseModel


class UserModelDTO(BaseModel):
    """
    DTO for user models.

    It returned when accessing user models from the API.
    """

    id: int
    name: str
    username: str

    class Config:
        orm_mode = True


class UserModelInputDTO(BaseModel):
    """DTO for creating new user model."""

    name: str
