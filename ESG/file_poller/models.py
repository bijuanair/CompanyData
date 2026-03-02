from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class ListedCompany(Base):
    __tablename__ = "listed_companies"
    __table_args__ = {"schema": "esg"}

    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), unique=True, nullable=False)
    company_name = Column(Text)
    isin = Column(String(20))
    exchange = Column(String(10), default="NSE")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())


class RawFiling(Base):
    __tablename__ = "raw_filings"
    __table_args__ = {"schema": "esg"}

    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), nullable=False)
    filing_type = Column(String(100))
    filing_date = Column(Date)
    financial_year = Column(String(20))
    announcement_subject = Column(Text)
    source_url = Column(Text, nullable=False)
    exchange = Column(String(10), default="NSE")
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())