from pydantic import BaseModel


class AuthModelDTO(BaseModel):
    """
    DTO for user models.

    It returned when accessing user models from the API.
    """

    access_token: str
    token_type: str

    class Config:
        orm_mode = False


# class AuthModelInputDTO(BaseModel):
#     """DTO for creating new user model."""

#     name: str
