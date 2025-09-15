from datetime import datetime

from langchain_core.output_parsers import JsonOutputParser
from sqlalchemy.orm import Session
from fastapi import WebSocket

from db.database import get_db
from executors.chain_executors import get_chain_executor
from models.investment_rating import InvestmentRating
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
        result = None
        async for chunk in get_chain_executor().astream({"input": f"请分析 股票 {stock_code} 的近期行情",
                                    "chat_history": []}):
            try:
                print(chunk["messages"][-1])
                chunk["messages"][-1].pretty_print()
                result = chunk["messages"][-1].content
                await websocket.send_text(chunk["messages"][-1].content)
            except Exception as ex:
                print(f"发送股票 {stock_code} 分析失败: {ex}")
        print(result)
        parser = JsonOutputParser(pydantic_object=StockReport)
        parsed_result = parser.parse(result["output"])
        print("parsed_result",parsed_result)
        db: Session = next(get_db())
        # 假设result中包含symbol和name信息
        rating_record = InvestmentRating(
            symbol=parsed_result.get('symbol', ''),
            name=parsed_result.get('name', ''),
            rating=parsed_result['investment_rating'],
            current_price=parsed_result.get('current_price', None),
            target_price=parsed_result.get('target_price', None),
            analysis_date=datetime.strptime(parsed_result.get('analysis_date', ''), '%Y-%m-%d') if result.get(
                'analysis_date') else None,
            result_json=parsed_result
        )
        db.add(rating_record)
        db.commit()
        db.refresh(rating_record)
        return parsed_result
    except Exception as e:
        print(f"股票 {stock_code} 分析失败: {e}")
        return None

