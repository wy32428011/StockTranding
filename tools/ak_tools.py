import os

import numpy as np
import pandas as pd
from langchain.tools import tool
import akshare as ak
from datetime import datetime, timedelta
import talib as ta
import os

from talib import MA_Type


# === 工具1：获取股票一周历史行情 ===
@tool
def get_stock_history(symbol: str) -> str:
    """
    获取近30天股票日线历史行情
    :param symbol: 股票编码
    :return:
    """
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
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
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
    print("===============================开始获取技术指标数据=======================================")
    df = ak.stock_zh_a_hist(symbol=symbol, period="daily",
                            start_date=(datetime.now() - timedelta(days=60)).strftime("%Y%m%d"), adjust="")
    close = pd.to_numeric(df["收盘"])
    high_prices = pd.to_numeric(df["最高"])
    low_prices = pd.to_numeric(df["最低"])
    ma5 = ta.MA(close, timeperiod=5)
    ma10 = ta.MA(close, timeperiod=10)
    macd, macd_signal, macd_hist = ta.MACD(close)
    rsi = ta.RSI(close, timeperiod=14)
    slowk, slowd = ta.STOCH(
        high_prices, low_prices, close,
        fastk_period=9, slowk_period=3, slowk_matype=MA_Type.SMA,
        slowd_period=3, slowd_matype=MA_Type.SMA
    )
    # 计算J值
    slowj = 3 * slowk - 2 * slowd
    # 计算布林带三线
    upper, middle, lower = ta.BBANDS(
        close,
        timeperiod=20,  # 默认周期
        nbdevup=2,  # 上轨标准差倍数
        nbdevdn=2,  # 下轨标准差倍数
        matype=MA_Type.SMA,   # 移动平均类型（0=SMA）
    )
    return {
        "MA5": ma5,
        "MA10": ma10,
        "MACD": macd,
        "RSI": rsi,
        "SLOWK": slowk,
        "SLOWD": slowd,
        "SLOWJ": slowj,
        "UPPER": upper,
        "MIDDLE": middle,
        "LOWER": lower,
    }


@tool
def get_stock_info_csv(symbol: str) -> str:
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