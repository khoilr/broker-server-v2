from datetime import datetime

from pydantic import BaseModel


class PredefinedReturnOutputDTO(BaseModel):
    """output DTO for Predifined Return model."""

    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    label: str
