# This is the 'store_to_sqlite.py' script
import sqlite3
import pandas as pd
import os

def store_to_sqlite():
    ROOT_DIR = r"D:\StockAnalysisProject"
    DATA_DIR = os.path.join(ROOT_DIR, "data")
    DB_FILE = os.path.join(DATA_DIR, "stock_data.db")
    CSV_FILE = os.path.join(DATA_DIR, "a_stock_data.csv")

    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS a_stock (
            code TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            change REAL,
            volume REAL,
            turnover REAL
        )
    """)
    print(f"A 股数据表已创建！数据库路径：{DB_FILE}")

    try:
        df_a = pd.read_csv(CSV_FILE)
        df_a.rename(columns={
            '代码': 'code',
            '名称': 'name',
            '最新价': 'price',
            '涨跌幅': 'change',
            '成交量': 'volume',
            '成交额': 'turnover'
        }, inplace=True)
        df_a['code'] = df_a['code'].astype(str)

        df_a.to_sql("a_stock", conn, if_exists="replace", index=False)
        print("A 股数据已成功存入数据库！")
    except Exception as e:
        print(f"存储数据失败：{e}")
    finally:
        conn.commit()
        conn.close()
