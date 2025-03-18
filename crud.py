from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from models import MutualFund, FundAllocation, FundOverlap
from typing import List, Dict, Any, Optional

# Get all mutual funds
async def get_mutual_funds(db: AsyncSession) -> List[MutualFund]:
    result = await db.execute(select(MutualFund))
    return result.scalars().all()

# Get mutual fund allocations
async def get_fund_allocations(db: AsyncSession, fund_id: int) -> List[FundAllocation]:
    result = await db.execute(select(FundAllocation).where(FundAllocation.fund_id == fund_id))
    return result.scalars().all()

# Get fund overlaps
async def get_fund_overlaps(db: AsyncSession) -> List[FundOverlap]:
    result = await db.execute(select(FundOverlap))
    return result.scalars().all()

# Get investment overview
async def get_investment_overview(db: AsyncSession) -> Dict[str, Any]:
    # Fetch total initial investment value
    initial_value_query = await db.execute(select(func.sum(MutualFund.amount_invested)))
    initial_value = initial_value_query.scalar() or 0.0

    # Fetch current investment value (considering returns)
    current_value_query = await db.execute(
        select(func.sum(MutualFund.amount_invested * (1 + MutualFund.returns_percentage / 100)))
    )
    current_value = current_value_query.scalar() or 0.0

    # Fetch best performing scheme
    best_performing_fund_query = await db.execute(
        select(MutualFund.name, MutualFund.returns_percentage)
        .order_by(MutualFund.returns_percentage.desc())
        .limit(1)
    )
    best_performing_fund = best_performing_fund_query.fetchone()
    
    best_fund_name: Optional[str] = best_performing_fund[0] if best_performing_fund else "N/A"
    best_fund_return: float = round(best_performing_fund[1], 2) if best_performing_fund else 0.0

    # Fetch worst performing scheme
    worst_performing_fund_query = await db.execute(
        select(MutualFund.name, MutualFund.returns_percentage)
        .order_by(MutualFund.returns_percentage.asc())
        .limit(1)
    )
    worst_performing_fund = worst_performing_fund_query.fetchone()

    worst_fund_name: Optional[str] = worst_performing_fund[0] if worst_performing_fund else "N/A"
    worst_fund_return: float = round(worst_performing_fund[1], 2) if worst_performing_fund else 0.0

    return {
        "current_investment_value": round(current_value, 2),
        "initial_investment_value": round(initial_value, 2),
        "best_performing_scheme": {
            "name": best_fund_name,
            "returns": best_fund_return
        },
        "worst_performing_scheme": {
            "name": worst_fund_name,
            "returns": worst_fund_return
        },
    }
