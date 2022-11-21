"""Dummy data model definition."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from .database import Base


class StockValue(Base):
    """Stock value data model."""

    __tablename__ = "stock_value"
    id = Column(Integer, primary_key=True)
    symbol_str = Column(String)
    date = Column(DateTime)
    open_num = Column(Float)
    low_num = Column(Float)
    high_num = Column(Float)
    close_num = Column(Float)
    volume_num = Column(Integer)
    created_at_dt = Column(DateTime(), default=datetime.utcnow)
    
    def __init__(self, symbol_str, date, open_num, low_num, high_num, close_num, volume_num):
        self.symbol_str = symbol_str
        self.date = date
        self.open_num = open_num
        self.low_num = low_num
        self.high_num = high_num
        self.close_num = close_num
        self.volume_num = volume_num
    
    def __repr__(self):
        return f"<StockValue(symbol='{self.symbol}', date='{self.date}', open='{self.open}', high='{self.high}', low='{self.low}', close='{self.close}', volume='{self.volume}')>"
    
    def __str__(self):
        return self.symbol_str
    
class CompanyOverview(Base):
    '''Company overview data model'''
    
    __tablename__ = "company_overview"
    symbol_str = Column(String, primary_key=True)
    asset_type_str = Column(String)
    name_str = Column(String)
    currency_str = Column(String)
    description_str = Column(String)
    exchange_str = Column(String)
    country_str = Column(String)
    sector_str = Column(String)
    industry_str = Column(String)
    created_at_dt = Column(DateTime(), default=datetime.utcnow)
    
    def __init__(self, symbol_str, asset_type_str, name_str, currency_str, description_str, exchange_str, country_str, sector_str, industry_str):
        self.symbol_str = symbol_str
        self.asset_type_str = asset_type_str
        self.name_str = name_str
        self.currency_str = currency_str
        self.description_str = description_str
        self.exchange_str = exchange_str
        self.country_str = country_str
        self.sector_str = sector_str
        self.industry_str = industry_str
    
    def __repr__(self):
        return f"<CompanyOverview(symbol='{self.symbol}', asset_type='{self.asset_type}', name='{self.name}', currency='{self.currency}', description='{self.description}', exchange='{self.exchange}', country='{self.country}', sector='{self.sector}', industry='{self.industry}')>"
    
    def __str__(self):
        return self.symbol_str