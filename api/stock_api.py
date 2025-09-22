import pandas as pd
from fastapi import APIRouter, WebSocket

from trading.process import process_stock_chunk_with_chain_ws

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
                df = pd.read_csv('./synchronization/A股code.csv',
                                 encoding='utf-8',
                                 dtype={'Code': str})
                df = df['Code'].tolist()
                for code in df:
                    code_o = code.split('.')[0]
                    await process_stock_chunk_with_chain_ws(code_o, websocket)

    except Exception as ex:
        print(f"股票实时行情 WebSocket 连接异常: {ex}")
