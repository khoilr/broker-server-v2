from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from server.db.dao.dummy import DummyDAO
from server.db.models.dummy import DummyModel
from server.web.api.dummy.schema import DummyDTO, DummyModelInputDTO

router = APIRouter()


@router.get("/", response_model=List[DummyDTO])
async def get_dummy_models(
    limit: int = 10,
    offset: int = 0,
    dummy_dao: DummyDAO = Depends(),
) -> List[DummyModel]:
    """
    Retrieve all dummy objects from the database.

    Args:
        limit (int): limit of dummy objects. Defaults to 10.
        offset (int): objects. Defaults to 0.
        dummy_dao (DummyDAO): DAO for dummy models. Defaults to Depends().

    Returns:
        List[DummyModel]: list of dummy objects from database.
    """
    return await dummy_dao.get_all_dummies(limit=limit, offset=offset)


@router.put("/")
async def create_dummy_model(
    new_dummy_object: DummyModelInputDTO,
    dummy_dao: DummyDAO = Depends(),
) -> None:
    """
    Creates dummy model in the database.

    Args:
        new_dummy_object (DummyModelInputDTO): new dummy model item.
        dummy_dao (DummyDAO): DAO for dummy models.. Defaults to Depends().

    Returns:
        None: None
    """
    await dummy_dao.create_dummy_model(**new_dummy_object.dict())
    return
