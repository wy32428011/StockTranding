from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT

from db.database import Base


class StockDataReport(Base):
    """股票数据报告"""
    __tablename__ = "stock_data_reports"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)  # 股票代码
    name = Column(String(100))  # 股票名称
    analysis_date = Column(DateTime, default=datetime.utcnow)
    analysis_content = Column(LONGTEXT)  # 分析内容
