from datetime import datetime
from typing import TypedDict, Annotated, Literal

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT

from db.database import Base


class StockAnalysisMarkdown(Base):
    """
    股票分析Markdown模型

    该模型用于存储股票的分析结果，包括基本面分析、交易数据动态分析、技术指标信号解读、综合研判与投资策略以及结论。
    """
    __tablename__ = "stock_analysis_markdowns"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False,comment="股票代码")  # 股票代码
    stock_name = Column(String(100),comment="股票名称")  # 股票名称
    analysis_date = Column(DateTime, default=datetime.utcnow,comment="分析日期")  # 分析日期
    fundamental_analysis = Column(LONGTEXT,comment="基本面分析")  # 分析内容
    trading_data_dynamic_analysis = Column(LONGTEXT,comment="交易数据动态分析")  # 分析内容
    technical_indicator_analysis = Column(LONGTEXT,comment="技术指标信号解读")  # 分析内容
    comprehensive_judgment_and_investment_strategy = Column(LONGTEXT,comment="综合研判与投资策略")  # 分析内容
    conclusion = Column(LONGTEXT,comment="结论")  # 分析内容

class StockAnalysisMarkdownModel(BaseModel):
    """
    股票分析Markdown模型

    该模型用于存储股票的分析结果，包括基本面分析、交易数据动态分析、技术指标信号解读、综合研判与投资策略以及结论。
    """
    symbol:str = Field(description="股票代码")  # 股票代码
    stock_name: str = Field(description="股票名称")  # 股票名称
    analysis_date: datetime = Field(description="分析日期")  # 分析日期
    fundamental_analysis: str = Field(description="基本面分析,markdown格式")  # 分析内容
    trading_data_dynamic_analysis: str = Field(description="交易数据动态分析,markdown格式")  # 分析内容
    technical_indicator_analysis: str = Field(description="技术指标信号解读,markdown格式")  # 分析内容
    comprehensive_judgment_and_investment_strategy: str = Field(description="综合研判与投资策略,markdown格式")  # 分析内容
    conclusion: str = Field(description="结论,markdown格式")  # 分析内容
    risk_level: Literal["低", "中", "高"] = Field(..., description="综合风险等级：低、中、高")
    investment_rating: Literal["强烈买入", "买入", "中性", "卖出", "强烈卖出"] = Field(..., description="投资评级：强烈买入、买入、中性、卖出、强烈卖出,该字段必须存在")
    buy_duration: str = Field(description="买入时长,例如：1年、3月、1周等")
