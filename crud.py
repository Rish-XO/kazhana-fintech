from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from models import MutualFund, FundAllocation, FundOverlap
from typing import List, Dict, Any, Optional
from datetime import date, timedelta,datetime
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

async def get_performance_summary(db: AsyncSession, timeframe: str) -> Dict[str, Any]:
    """
    Returns investment growth based on fund purchase date.
    Uses timeframes: "1M", "3M", "6M", "1Y", "3Y", "MAX".
    """
    # Fetch total initial investment value
    initial_value_query = await db.execute(select(func.sum(MutualFund.amount_invested)))
    initial_value = initial_value_query.scalar() or 0.0
    initial_value = float(initial_value)  # Convert Decimal to float

    # Get the oldest purchase date
    oldest_date_query = await db.execute(select(func.min(MutualFund.investment_date)))
    oldest_date = oldest_date_query.scalar()
    if not oldest_date:
        return {"message": "No investments found."}

    # Calculate starting date based on timeframe
    today = datetime.today().date()
    timeframe_map = {
        "1M": today - timedelta(days=30),
        "3M": today - timedelta(days=90),
        "6M": today - timedelta(days=180),
        "1Y": today - timedelta(days=365),
        "3Y": today - timedelta(days=3 * 365),
        "MAX": oldest_date,
    }
    start_date = timeframe_map.get(timeframe, oldest_date)

    # Simulate performance growth using investment date
    history = []
    days_range = (today - start_date).days
    for i in range(0, days_range, max(days_range // 7, 1)):  # 7 data points
        date = start_date + timedelta(days=i)
        growth_factor = 1 + (i / 1000)  # Simulated growth
        simulated_value = initial_value * growth_factor  # Fix applied here
        history.append({"date": date.strftime("%d %b"), "value": round(simulated_value, 2)})

    # Fetch current investment value
    current_value_query = await db.execute(
        select(func.sum(MutualFund.amount_invested * (1 + MutualFund.returns_percentage / 100)))
    )
    current_value = current_value_query.scalar() or 0.0
    current_value = float(current_value)  # Convert Decimal to float

    return {
        "current_investment_value": round(current_value, 2),
        "initial_investment_value": round(initial_value, 2),
        "history": history,
    }


# Get Sector Allocation API
async def get_sector_allocation(db: AsyncSession) -> List[Dict[str, Any]]:
    # Fetch outer sector allocations
    sector_query = await db.execute(
        select(
            FundAllocation.sector,
            func.sum(FundAllocation.sector_amount).label("total_amount"),
            func.sum(FundAllocation.sector_percentage).label("total_percentage"),
        ).group_by(FundAllocation.sector)
    )
    sectors = sector_query.fetchall()

    # Fetch sub-sector allocations (stocks in each sector)
    sub_sector_query = await db.execute(
        select(
            FundAllocation.sector,
            FundAllocation.stock,
            FundAllocation.stock_percentage,
            FundAllocation.sector_amount
        )
    )
    sub_sector_data = sub_sector_query.fetchall()

    # Organize data into expected response format
    sector_allocation = []
    sub_sector_map = {}

    for sector, stock, stock_percentage, sector_amount in sub_sector_data:
        if sector not in sub_sector_map:
            sub_sector_map[sector] = []
        sub_sector_map[sector].append({
            "name": stock,
            "percentage": float(stock_percentage),
            "amount": float(sector_amount)
        })

    for sector, total_amount, total_percentage in sectors:
        sector_allocation.append({
            "name": sector,
            "amount": float(total_amount),
            "percentage": float(total_percentage),
            "sub_allocations": sub_sector_map.get(sector, [])  # Attach sub-sector data
        })

    return sector_allocation
