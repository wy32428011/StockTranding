from typing import List

from pydantic import BaseModel

from models.stock_info import StockInfo


class DataInfo(BaseModel):
    static_info_list: List[StockInfo]

class StockInfoResponse(BaseModel):
    ret: str
    msg: str
    trace: str
    data: DataInfo


