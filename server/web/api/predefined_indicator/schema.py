from datetime import datetime

from pydantic import BaseModel

from server.web.api.predefined_param.schema import PredefinedParamOutputModelDTO
from server.web.api.predefined_return.schema import PredefinedReturnOutputModelDTO


class PredefinedIndicatorOutputModelDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    label: str
    predefined_params: list[PredefinedParamOutputModelDTO]
    predefined_returns: list[PredefinedReturnOutputModelDTO]
