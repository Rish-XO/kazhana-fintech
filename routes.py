from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud import get_mutual_funds,get_fund_allocations, get_fund_overlaps, get_investment_overview, get_performance_summary,get_sector_allocation,get_fund_overlap_data
from schemas import MutualFundResponse, FundAllocationResponse, FundOverlapResponse
from typing import Dict,List, Any 

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

@router.get("/performance_summary", response_model=Dict[str, Any])
async def fetch_performance_summary(
    timeframe: str = Query("1M", description="Timeframe for investment performance"),
    db: AsyncSession = Depends(get_db),
):
    return await get_performance_summary(db, timeframe)

@router.get("/sector_allocation", response_model=List[Dict[str, Any]])
async def fetch_sector_allocation(db: AsyncSession = Depends(get_db)):
    return await get_sector_allocation(db)

@router.get("/fund_overlap", response_model=Dict[str, Any])
async def fetch_fund_overlap(db: AsyncSession = Depends(get_db)):
    """
    API to get fund-stock overlap data for Sankey chart
    """
    return await get_fund_overlap_data(db)