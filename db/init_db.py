from db.database import Base, engine
from models.stock_data_report import StockDataReport
# 创建所有数据库表
Base.metadata.create_all(bind=engine)
print("数据库表创建成功!")
# 关闭数据库连接
engine.dispose()
