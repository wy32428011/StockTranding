from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from setting.config_setting import DB_CONFIG

# MySQL数据库配置
MYSQL_USER = str(DB_CONFIG.get("user"))  # 替换为你的MySQL用户名
MYSQL_PASSWORD = str(DB_CONFIG.get("password"))  # 替换为你的MySQL密码
MYSQL_HOST = str(DB_CONFIG.get("host"))  # 替换为你的MySQL主机
MYSQL_PORT = int(DB_CONFIG.get("port"))  # 替换为你的MySQL端口
MYSQL_DB = str(DB_CONFIG.get("database"))  # 替换为你的MySQL数据库名

# 创建数据库连接
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 数据库依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
