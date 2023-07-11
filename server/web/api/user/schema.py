from pydantic import BaseModel


class UserOutputModelDTO(BaseModel):
    id: int
    name: str
    username: str

    class Config:
        orm_mode = True


class UserModelInputDTO(BaseModel):
    name: str
