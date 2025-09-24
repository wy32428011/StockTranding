import asyncio
import json
from datetime import datetime

from langchain_core.output_parsers import JsonOutputParser
from sqlalchemy.orm import Session
from fastapi import WebSocket

from db.database import get_db
from executors.chain_executors import get_chain_executor, get_chain_executor_stock_analysis
from models.investment_rating import InvestmentRating
from models.stock_data_report import StockDataReport
from models.stock_report import StockReport


async def process_stock_chunk_with_chain_ws(stock_code: str, websocket: WebSocket):
    """
    处理一个股票代码块的函数，使用异步方式调用链执行器，并将结果通过WebSocket发送。

    :param stock_code: 股票代码
    :param websocket: WebSocket连接对象
    :return: 解析后的股票报告对象
    """
    try:
        # result = get_executor().invoke({"input": f"请分析 股票 {stock_code} 的近期行情",
        #                                 "chat_history": []})
        result = ''
        async for chunk in get_chain_executor().astream({"input": f"请分析 股票 {stock_code} 的近期行情",
                                    "chat_history": []}):
            try:
                print(chunk["messages"][-1])
                chunk["messages"][-1].pretty_print()
                result = chunk["messages"][-1].content
                if result:
                    await websocket.send_text(result)
            except Exception as ex:
                print(f"发送股票 {stock_code} 分析失败: {ex}")
        print(result)

        ss_result = result
        if result.find("</think>") != -1:
            ss_result = result.split("</think>")[1]
        print(f"股票 {stock_code} 分析内容:\n {ss_result}")
        db: Session = next(get_db())
        stock_data_report = StockDataReport(
            symbol=stock_code,
            analysis_content=ss_result,
            analysis_date=datetime.utcnow()
        )
        db.add(stock_data_report)
        db.commit()
        db.refresh(stock_data_report)
        # await get_chain_executor_stock_analysis(stock_code,ss_result)
        return result
    except Exception as e:
        print(f"股票 {stock_code} 分析失败: {e}")
        await websocket.send_text(f"股票 {stock_code} 分析失败: {e}")
        return None

async def process_stock_chunk_with_chain_ws_analysis(stock_code: list, websocket: WebSocket):
    """
    :param stock_code: 股票代码列表
    :param websocket: WebSocket连接对象
    :return: 无
    """
    # TODO: 多线程调用process_stock_chunk_with_chain_ws方法来处理股票代码列表
    """
       :param stock_code: 股票代码列表
       :param websocket: WebSocket连接对象
       :param max_concurrent_tasks: 最大并发任务数(线程数)，默认5
       :return: 无
       """
    if not stock_code:
        await websocket.send_text("股票代码列表为空，无需处理")
        return
    max_concurrent_tasks = 6
    # 确保并发任务数至少为1
    max_concurrent_tasks = max(1, max_concurrent_tasks)

    # 分割股票列表为多个块，每个块包含最多max_concurrent_tasks个股票代码
    def split_into_chunks(lst, chunk_size):
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

    chunks = split_into_chunks(stock_code, max_concurrent_tasks)
    total_chunks = len(chunks)

    await websocket.send_text(
        f"开始处理股票列表，共{len(stock_code)}支股票，分为{total_chunks}个块，每块最多{max_concurrent_tasks}支股票")

    for chunk_idx, chunk in enumerate(chunks, 1):
        await websocket.send_text(f"开始处理第{chunk_idx}/{total_chunks}块，包含股票: {chunk}")
        try:
            # 为当前块中的每个股票创建处理任务
            tasks = [process_stock_chunk_with_chain_ws(stock, websocket) for stock in chunk]
            # 并发执行当前块的所有任务
            await asyncio.gather(*tasks)
            await websocket.send_text(f"第{chunk_idx}/{total_chunks}块处理完成")
        except Exception as e:
            await websocket.send_text(f"处理第{chunk_idx}/{total_chunks}块时发生错误: {str(e)}")