from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import MutualFund, FundAllocation, FundOverlap

# Get all mutual funds
async def get_mutual_funds(db: AsyncSession):
    result = await db.execute(select(MutualFund))
    return result.scalars().all()

# Get mutual fund allocations
async def get_fund_allocations(db: AsyncSession, fund_id: int):
    result = await db.execute(select(FundAllocation).where(FundAllocation.fund_id == fund_id))
    return result.scalars().all()

# Get fund overlaps
async def get_fund_overlaps(db: AsyncSession):
    result = await db.execute(select(FundOverlap))
    return result.scalars().all()
