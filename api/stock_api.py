
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
