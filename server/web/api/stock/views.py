import json

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from server.db.dao.stock_dao import StockDAO
from server.db.models.stock_model import StockModel
from server.web.api.stock.schema import StockOutputModelDTO

router = APIRouter()


@router.get("/", response_model=list[StockOutputModelDTO])
async def get_stocks(stock_dao: StockDAO = Depends()) -> list[StockModel]:
    return await stock_dao.get_all()
