from datetime import datetime

from pydantic import BaseModel


class PredefinedParamOutputModelDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    label: str
    type: str
