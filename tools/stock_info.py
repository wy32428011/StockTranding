import asyncio
import akshare as ak

async def get_stock_info():
    """
    获取股票信息
    :param symbol: 股票编码
    :return: 股票信息
    """
    await asyncio.sleep(0.1)
    # 获取所有A股实时行情数据（含股票代码）
    data = ak.stock_zh_a_spot_em()
    # 提取股票代码列
    stock_codes = data["代码"].tolist()
    data_all = data[['序号', '代码', '名称', '最新价', '涨跌幅', '涨跌额', '成交量',
                     '成交额', '振幅', '最高', '最低', '今开', '昨收', '量比',
                     '换手率', '市盈率-动态', '市净率', '总市值', '流通市值', '涨速', '5分钟涨跌',
                     '60日涨跌幅', '年初至今涨跌幅']]
    print(f"共获取 {len(stock_codes)} 只A股股票代码")

    data_all.to_csv("A股股票列表.csv", index=False, encoding="utf_8")


# asyncio.run(get_stock_info())
