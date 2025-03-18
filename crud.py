from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from models import MutualFund, FundAllocation, FundOverlap
from typing import List, Dict, Any, Optional
from datetime import date, timedelta
import decimal

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

    # initial investment percentage calculation
    overall_return_percentage = (
    ((current_value - initial_value) / initial_value) * 100 if initial_value != 0 else 0
)

    return {
        "current_investment_value": round(current_value, 2),
        "initial_investment_value": round(initial_value, 2),
         "initial_investment_growth": round(overall_return_percentage, 2),  
        "best_performing_scheme": {
            "name": best_fund_name,
            "returns": best_fund_return
        },
        "worst_performing_scheme": {
            "name": worst_fund_name,
            "returns": worst_fund_return
        },
    }

def calculate_irr(initial_value: float, returns_percentage: float, days: int) -> float:
    """
    Estimate investment value over time using a simplified IRR calculation.
    Since we lack daily NAV history, we assume exponential growth.
    """
    if days <= 0:
        return initial_value
    growth_factor = (1 + (returns_percentage / 100)) ** (days / 365)  # Annualized compounding
    return initial_value * growth_factor

async def get_performance_summary(db: AsyncSession) -> Dict[str, Any]:
    # Fetch total initial investment value
    initial_value_query = await db.execute(select(func.sum(MutualFund.amount_invested)))
    initial_value = initial_value_query.scalar() or decimal.Decimal(0)

    # Fetch total current investment value (based on returns)
    current_value_query = await db.execute(
        select(func.sum(MutualFund.amount_invested * (1 + MutualFund.returns_percentage / 100)))
    )
    current_value = current_value_query.scalar() or decimal.Decimal(0)

    # Convert Decimal to float
    initial_value = float(initial_value)
    current_value = float(current_value)

    # Get the oldest investment date
    oldest_investment_date_query = await db.execute(select(func.min(MutualFund.investment_date)))
    oldest_investment_date = oldest_investment_date_query.scalar() or date.today()

    today = date.today()
    days_since_first_investment = (today - oldest_investment_date).days

    # Generate estimated historical performance data
    history = []
    days_range = 30  # Show last 30 days
    for days_ago in range(days_range, -1, -5):  # Generate every 5 days
        past_date = today - timedelta(days=days_ago)
        estimated_value = calculate_irr(initial_value, (current_value - initial_value) / initial_value * 100, days_since_first_investment - days_ago)
        history.append({
            "date": past_date.strftime("%d %b"),  # Format as "DD Mon"
            "value": round(estimated_value, 2)
        })

    return {
        "current_investment_value": round(current_value, 2),
        "initial_investment_value": round(initial_value, 2),
        "history": history
    }
