from pydantic import BaseModel


class UserOutputDTO(BaseModel):
    """User model for Output DTO."""

    id: int
    name: str
    username: str

    class Config:
        orm_mode = True


class UserModelInputDTO(BaseModel):
    """User model for Input DTO."""

    name: str
