from pydantic import BaseModel


class ParamInputDTO(BaseModel):
    """Input DTO for Parameters model."""

    name: str
    value: str
