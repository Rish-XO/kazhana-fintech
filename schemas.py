from pydantic import BaseModel
from datetime import date

class MutualFundResponse(BaseModel):
    id: int
    name: str
    investment_date: date
    amount_invested: float
    isn: str
    nav_at_investment: float
    returns_percentage: float

    class Config:
        orm_mode = True

class FundAllocationResponse(BaseModel):
    fund_id: int
    sector: str
    sector_percentage: float
    stock: str
    stock_percentage: float
    market_cap: str

    class Config:
        orm_mode = True

class FundOverlapResponse(BaseModel):
    fund_1_id: int
    fund_2_id: int
    overlap_percentage: float

    class Config:
        orm_mode = True
