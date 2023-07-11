from pydantic import BaseModel


class AuthModelDTO(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = False


# class AuthModelInputDTO(BaseModel):
#     """DTO for creating new user model."""

#     name: str
