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
        db: Session = next(get_db())
        stock_data_report = StockDataReport(
            symbol=stock_code,
            analysis_content=result,
            analysis_date=datetime.utcnow()
        )
        db.add(stock_data_report)
        db.commit()
        db.refresh(stock_data_report)
        # if result.startswith("{'properties':"):
        #     result = result.replace("{'properties':","").rstrip("}")
        # parser = JsonOutputParser(pydantic_object=StockReport)
        # parsed_result = parser.parse(result)
        # print("parsed_result",parsed_result)
        # db: Session = next(get_db())
        # 假设result中包含symbol和name信息
        # rating_record = InvestmentRating(
        #     symbol=parsed_result.get('symbol', ''),
        #     name=parsed_result.get('name', ''),
        #     rating=parsed_result['investment_rating'],
        #     current_price=parsed_result.get('current_price', None),
        #     target_price=parsed_result.get('target_price', None),
        #     analysis_date=datetime.strptime(parsed_result.get('analysis_date', ''), '%Y-%m-%d') if parsed_result.get(
        #         'analysis_date') else None,
        #     result_json=parsed_result
        # )
        # db.add(rating_record)
        # db.commit()
        # db.refresh(rating_record)
        ss_result = result
        if result.find("</think>") != -1:
            ss_result = result.split("</think>")[1]
        print(f"股票 {stock_code} 分析内容:\n {ss_result}")
        await get_chain_executor_stock_analysis(stock_code,ss_result)
        return result
    except Exception as e:
        print(f"股票 {stock_code} 分析失败: {e}")
        await websocket.send_text(f"股票 {stock_code} 分析失败: {e}")
        return None

