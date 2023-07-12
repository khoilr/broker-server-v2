from pydantic import BaseModel
from datetime import datetime


class PredefinedParamOutputModelDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    label: str
    type: str
