import json

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from server.db.dao.stock_dao import StockDAO
from server.db.models.stock_model import StockModel

router = APIRouter()


@router.get("/")
async def get_stocks(stock_dao: StockDAO = Depends()):
    return await stock_dao.get_all()
