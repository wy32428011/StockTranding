import os

import pandas as pd
from langchain.tools import tool
import akshare as ak
from datetime import datetime, timedelta
import talib as ta

# === 工具1：获取股票一周历史行情 ===
@tool
def get_stock_history(symbol: str) -> str:
    """
    获取近30天股票日线历史行情
    :param symbol: 股票编码
    :return:
    """
    print("===============================开始获取30天历史数据=======================================")
    end = datetime.now()
    start = end - timedelta(days=30)
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start.strftime("%Y%m%d"), adjust="")
    return df.tail(30).to_string(index=False)

@tool
def tech_tool(symbol: str) -> dict:
    """
    计算技术指标：计算MA5/MA10、MACD、RSI
    :param symbol: 股票编码
    :return: 技术指标数据
    """
    print("===============================开始获取技术指标数据=======================================")
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily",
                            start_date=(datetime.now() - timedelta(days=60)).strftime("%Y%m%d"), adjust="")
    close = pd.to_numeric(df["收盘"])

    ma5 = ta.MA(close, timeperiod=5)
    ma10 = ta.MA(close, timeperiod=10)
    macd, macd_signal, macd_hist = ta.MACD(close)
    rsi = ta.RSI(close, timeperiod=14)
    print(ma5)
    return {
        "MA5": ma5,
        "MA10": ma10,
        "MACD": macd,
        "RSI": rsi
    }


@tool
def get_stock_info_csv(symbol: str):
    """
    获取股票信息
    :param symbol: 股票编码
    :return: 股票信息
    """
    # os.path.exists('./A股股票列表.csv')
    df = pd.read_csv('./tools/A股股票列表.csv',
                     encoding='utf-8',
                     dtype={'代码': str, '名称': str, '最新价': float})
    df = df[df["代码"] == symbol]
    return df.to_string(index=False)