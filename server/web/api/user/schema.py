from pydantic import BaseModel


class UserOutputDTO(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        orm_mode = True


class UserModelInputDTO(BaseModel):
    name: str
