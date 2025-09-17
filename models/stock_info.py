from sqlalchemy import Column, Integer, String, DateTime, JSON, Float

from datetime import datetime

from db.database import Base

from sqlalchemy import Column, Integer, String
from db.database import Base


class StockInfo(Base):
    __tablename__ = "stock_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment="自增主键")
    board = Column(String(255), nullable=True, comment="股票所属板块")
    bps = Column(String(255), nullable=True, comment="每股净资产")
    circulating_shares = Column(String(255), nullable=True, comment="流通股本")
    currency = Column(String(255), nullable=True, comment="交易币种")
    dividend_yield = Column(String(255), nullable=True, comment="股息")
    eps = Column(String(255), nullable=True, comment="每股盈利")
    eps_ttm = Column(String(255), nullable=True, comment="每股盈利 (TTM)")
    exchange = Column(String(255), nullable=True, comment="产品所属交易所")
    hk_shares = Column(String(255), nullable=True, comment="港股股本 (仅港股)")
    lot_size = Column(String(255), nullable=True, comment="每手股数")
    name_cn = Column(String(255), nullable=True, comment="中文简体产品的名称")
    name_en = Column(String(255), nullable=True, comment="英文产品的名称")
    name_hk = Column(String(255), nullable=True, comment="中文繁体产品的名称")
    symbol = Column(String(255), index=True, nullable=True, comment="产品code")
    total_shares = Column(String(255), nullable=True, comment="总股本")

