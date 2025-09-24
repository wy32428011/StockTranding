import pandas as pd
from fastapi import APIRouter, WebSocket

from executors.chain_executors import get_chain_executor_stock_analysis
from trading.process import process_stock_chunk_with_chain_ws, process_stock_chunk_with_chain_ws_analysis

stock_api = APIRouter()
@stock_api.websocket("/ws")
async def get_stock_spot_ws(websocket: WebSocket):
    """
    获取股票实时行情
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await process_stock_chunk_with_chain_ws(data, websocket)

    except Exception as ex:
        print(f"股票实时行情 WebSocket 连接异常: {ex}")

@stock_api.websocket("/all-stock-ws")
async def get_all_stock_spot_ws(websocket: WebSocket):
    """
    获取股票实时行情
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == 'all':
                df = pd.read_csv('./tools/A股股票列表.csv',
                                 encoding='utf-8',
                                 dtype={'代码': str,'名称': str})
                df = df['代码'].tolist()
                for code in df:
                    code_o = code.split('.')[0]
                    await process_stock_chunk_with_chain_ws(code_o, websocket)

    except Exception as ex:
        print(f"股票实时行情 WebSocket 连接异常: {ex}")
@stock_api.websocket("/all-stock-chunk-ws")
async def get_all_stock_chunk_spot_ws(websocket: WebSocket):
    """
    获取股票实时行情
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == 'all':
                df = pd.read_csv('./tools/A股股票列表.csv',
                                 encoding='utf-8',
                                 dtype={'代码': str,'名称': str,'最新价': float})
                df = df[df['最新价'] < 25]
                df = df['代码'].tolist()
                await process_stock_chunk_with_chain_ws_analysis(df, websocket)

    except Exception as ex:
        print(f"股票实时行情 WebSocket 连接异常: {ex}")
@stock_api.websocket("/all-stock-analysis-ws")
async def get_chain_executor_stock_analysis_ws(websocket: WebSocket):
    """
    获取股票分析链执行器
    :return:
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            if data:
                await get_chain_executor_stock_analysis(data['symbol'],data['content'])
    except Exception as ex:
        print(f"股票分析链执行器 WebSocket 连接异常: {ex}")
