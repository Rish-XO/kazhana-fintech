from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MutualFund(Base):
    __tablename__ = "mutual_funds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    investment_date = Column(Date, nullable=False)
    amount_invested = Column(Numeric(15,2), nullable=False)
    isn = Column(String, unique=True, nullable=False)
    nav_at_investment = Column(Numeric(10,2), nullable=False)
    returns_percentage = Column(Numeric(5,2), nullable=False)

class FundAllocation(Base):
    __tablename__ = "fund_allocations"

    id = Column(Integer, primary_key=True, index=True)
    fund_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    sector = Column(String, nullable=False)
    sector_percentage = Column(Numeric(5,2), nullable=False)
    stock = Column(String, nullable=False)
    stock_percentage = Column(Numeric(5,2), nullable=False)
    market_cap = Column(String, nullable=False)
    sector_amount = Column(Numeric(15,2), nullable=True)  # Added sector amount column
    sub_sector = Column(String, nullable=True)  # Added sub-sector column

class FundOverlap(Base):
    __tablename__ = "fund_overlaps"

    id = Column(Integer, primary_key=True, index=True)
    fund_1_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    fund_2_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    overlap_percentage = Column(Numeric(5,2), nullable=False)

class FundStockOverlap(Base):
    __tablename__ = "fund_stock_overlaps"

    id = Column(Integer, primary_key=True, index=True)
    fund_1_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    fund_2_id = Column(Integer, ForeignKey("mutual_funds.id"), nullable=False)
    stock = Column(String, nullable=False)
    overlap_percentage = Column(Numeric(5,2), nullable=False)
