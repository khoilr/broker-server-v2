from fastapi import APIRouter, Depends
from server.db.dao.predefined_indicator_dao import PredefinedIndicatorDAO

router = APIRouter()


@router.get("/")
async def get_predefined_indicators(predefined_indicator_dao: PredefinedIndicatorDAO = Depends()):
    predefined_indicators = await predefined_indicator_dao.get_all()
    data = []

    for predefined_indicator in predefined_indicators:
        # Get predefined params and returns
        predefined_params = [predefined_param for predefined_param in predefined_indicator.predefined_params]
        predefined_returns = [predefined_return for predefined_return in predefined_indicator.predefined_returns]

        # Build predefined indicator
        _predefined_indicator = {
            "name": predefined_indicator.name,
            "label": predefined_indicator.label,
            "id": predefined_indicator.id,
            "created_at": predefined_indicator.created_at,
            "updated_at": predefined_indicator.updated_at,
            "predefined_params": predefined_params,
            "predefined_returns": predefined_returns,
        }

        # Append to data
        data.append(_predefined_indicator)

    return data
