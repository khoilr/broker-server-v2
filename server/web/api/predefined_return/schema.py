from datetime import datetime

from pydantic import BaseModel


class PredefinedReturnOutputModelDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    label: str
