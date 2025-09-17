import time

import pandas as pd
import requests
import json

from sqlalchemy.orm import Session

from db.database import get_db
from models.stock_info import StockInfo

test_header = {
    "Content-Type": "application/json",
}
# 雪球token
alltick_token = "09ab7e110950969ece587b50aa87ede9-c-app"
# 雪球股票api基础地址
base_alltick_url = f"https://quote.alltick.io/quote-stock-b-api/static_info?token={alltick_token}&query="
max_query = 10
symbol_list = []
df = pd.read_csv('A股code.csv',
                     encoding='utf-8',
                     dtype={'Code': str})

df_list = df['Code'].tolist()
data_index = 0
db: Session = next(get_db())
table_symbols = [symbol[0] for symbol in db.query(StockInfo.symbol).all()]
new_symbols = list(set(df_list) - set(table_symbols))
print(f"共有 {len(new_symbols)} 只股票需要同步")
for symbol in new_symbols:
    data_index += 1
    symbol_list.append({"code": symbol})
    try:
        if data_index % max_query == 0:
            request_data = {
                "trace": "edd5df80-df7f-4acf-8f67-68fd2f096426",
                "data": {
                    "symbol_list": symbol_list
                }
            }

            request_url = f"{base_alltick_url}{json.dumps(request_data)}"
            response = requests.get(request_url, headers=test_header)
            if response.status_code == 200:
                print(f"成功获取 {data_index} 只股票数据")
                json_data = json.loads(response.content)["data"]["static_info_list"]
                for item in json_data:
                    try:
                        stock_info = StockInfo(**item)

                        db.add(stock_info)
                        db.commit()
                        db.refresh(stock_info)
                    except Exception as e:
                        print(f"添加 {item['code']} 股票数据失败，错误信息：{e}")
            else:
                print(f"获取 {data_index} 只股票数据失败，状态码：{response.status_code}")
            time.sleep(10)
            symbol_list = []
    except Exception as e:
        print(f"获取 {data_index} 只股票数据失败，错误信息：{e}")

"""
{
  "trace": "edd5df80-df7f-4acf-8f67-68fd2f096426",
  "data": {
    "symbol_list": [
      {
        "code": "857.HK"
      },
      {
        "code": "UNH.US"
      }
    ]
  }
}
"""