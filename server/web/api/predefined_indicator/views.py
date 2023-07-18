from typing import List

from fastapi import APIRouter, Depends

from server.db.dao.predefined_indicator import PredefinedIndicatorDAO
from server.web.api.predefined_indicator.schema import PredefinedIndicatorOutputDTO

router = APIRouter()


@router.get(
    "/",
    response_model=List[PredefinedIndicatorOutputDTO],
)
async def get_predefined_indicators(
    predefined_indicator_dao: PredefinedIndicatorDAO = Depends(),
):
    predefined_indicators = await predefined_indicator_dao.get_all()
    data = [
        {
            "name": predefined_indicator.name,
            "label": predefined_indicator.label,
            "id": predefined_indicator.id,
            "created_at": predefined_indicator.created_at,
            "updated_at": predefined_indicator.updated_at,
            "predefined_params": await predefined_indicator.predefined_params,  # type: ignore
            "predefined_returns": await predefined_indicator.predefined_returns,  # type: ignore
        }
        for predefined_indicator in predefined_indicators
    ]

    return data
