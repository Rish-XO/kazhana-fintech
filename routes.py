from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud import get_mutual_funds,get_fund_allocations, get_fund_overlaps, get_investment_overview
from schemas import MutualFundResponse, FundAllocationResponse, FundOverlapResponse

router = APIRouter(prefix="", tags=["mutual-funds"])

@router.get("/mutual_funds", response_model=list[MutualFundResponse])
async def fetch_mutual_funds(db: AsyncSession = Depends(get_db)):
    return await get_mutual_funds(db)

@router.get("/fund_allocations/{fund_id}", response_model=list[FundAllocationResponse])
async def fetch_fund_allocations(fund_id: int, db: AsyncSession = Depends(get_db)):
    return await get_fund_allocations(db, fund_id)

@router.get("/fund_overlaps", response_model=list[FundOverlapResponse])
async def fetch_fund_overlaps(db: AsyncSession = Depends(get_db)):
    return await get_fund_overlaps(db)


@router.get("/investment_overview")
async def fetch_investment_overview(db: AsyncSession = Depends(get_db)):
    print("Investment overview endpoint called")
    return await get_investment_overview(db)
