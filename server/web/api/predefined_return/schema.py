from pydantic import BaseModel
from datetime import datetime


class PredefinedReturnOutputModelDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    label: str
