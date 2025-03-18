from pydantic import BaseModel
from datetime import date
from typing import Optional

class MutualFundResponse(BaseModel):
    id: int
    name: str
    investment_date: date
    amount_invested: float
    isn: str
    nav_at_investment: float
    returns_percentage: float

    class Config:
        from_attributes = True  # Updated for Pydantic v2 (previously orm_mode)

class FundAllocationResponse(BaseModel):
    fund_id: int
    sector: str
    sector_percentage: float
    stock: str
    stock_percentage: float
    market_cap: str
    sector_amount: Optional[float] = None  # Added sector amount for frontend requirement
    sub_sector: Optional[str] = None  # Added optional sub-sector field

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
