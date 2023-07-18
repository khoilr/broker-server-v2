from typing import Union
from pydantic import BaseModel


class ParamInputDTO(BaseModel):
    name: str
    value: str
