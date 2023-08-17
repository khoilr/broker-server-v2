from datetime import datetime

from pydantic import BaseModel


class PredefinedParamOutputDTO(BaseModel):
    """Output DTO for Predifined Parameters model."""

    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    label: str
    type: str
