from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from api.stock_api import stock_api

app = FastAPI()
app.include_router(stock_api)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info")
