from pydantic import BaseModel
from datetime import date
from typing import Optional

class InvestmentOverviewResponse(BaseModel):
    current_investment_value: float
    initial_investment_value: float
    best_performing_scheme: str
    worst_performing_scheme: str

class MutualFundResponse(BaseModel):
    id: int
    name: str
    investment_date: date
    amount_invested: float
    isn: str
    nav_at_investment: float
    returns_percentage: float

    class Config:
        from_attributes = True  

class FundAllocationResponse(BaseModel):
    fund_id: int
    sector: str
    sector_percentage: float
    stock: str
    stock_percentage: float
    market_cap: str
    sector_amount: Optional[float] = None 
    sub_sector: Optional[str] = None  
    class Config:
        from_attributes = True

class FundOverlapResponse(BaseModel):
    fund_1_id: int
    fund_2_id: int
    overlap_percentage: float

    class Config:
        from_attributes = True

class FundStockOverlapResponse(BaseModel):
    fund_1_id: int
    fund_2_id: int
    stock: str
    overlap_percentage: float

    class Config:
        from_attributes = True
