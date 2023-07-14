from pydantic import BaseModel


class StrategyInputDTO(BaseModel):
    stocks: list[str]

    class Config:
        orm_mode = True
