from datetime import datetime

from pydantic import BaseModel

from server.web.api.predefined_param.schema import PredefinedParamOutputDTO
from server.web.api.predefined_return.schema import PredefinedReturnOutputDTO


class PredefinedIndicatorOutputDTO(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    label: str
    predefined_params: list[PredefinedParamOutputDTO]
    predefined_returns: list[PredefinedReturnOutputDTO]
