# This is the 'query_sqlite.py' script
import sqlite3
import os

# 文件根目录
ROOT_DIR = r"D:\StockAnalysisProject"  # 项目根目录
DATA_DIR = os.path.join(ROOT_DIR, "data")  # 数据文件夹
DB_FILE = os.path.join(DATA_DIR, "stock_data.db")  # 数据库文件路径

# 确保数据库文件存在
if not os.path.exists(DB_FILE):
    print(f"数据库文件不存在：{DB_FILE}")
    exit()

# 连接 SQLite 数据库
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 查询功能
def query_sqlite(sql_query):
    try:
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        print(f"查询结果（共 {len(rows)} 条）：")
        for row in rows:
            print(row)
    except Exception as e:
        print(f"查询失败，错误信息：{e}")

# 关闭数据库连接
def close_connection():
    conn.close()
