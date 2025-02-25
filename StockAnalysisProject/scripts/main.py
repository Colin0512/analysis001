import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from query_sqlite import query_sqlite  # 导入查询函数
from store_to_sqlite import store_to_sqlite  # 导入存储函数
from visualize_data import plot_k_line, plot_volume_and_change  # 导入可视化函数

# 设置中文字体
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示问题

# 设置绝对路径
ROOT_DIR = r"D:\StockAnalysisProject"  # 项目根目录
DATA_DIR = os.path.join(ROOT_DIR, "data")  # 数据文件夹
CSV_FILE = os.path.join(DATA_DIR, "a_stock_data.csv")  # CSV 文件路径
DB_FILE = os.path.join(DATA_DIR, "stock_data.db")  # 数据库文件路径

# 主程序
def main():
    # 1. 存储数据到 SQLite
    print("开始存储数据到 SQLite...")
    store_to_sqlite()

    # 2. 确认 CSV 文件存在
    if not os.path.exists(CSV_FILE):
        print(f"文件 {CSV_FILE} 不存在，请确保文件路径正确。")
        return  # 退出程序

    # 3. 读取 CSV 文件并查看列名
    df_a = pd.read_csv(CSV_FILE, encoding='utf-8')  # 加载时指定编码
    print(f"CSV 文件的列名：{df_a.columns}")
    
    # 强制转换为数值类型
    df_a['price'] = pd.to_numeric(df_a['price'], errors='coerce')
    df_a['change'] = pd.to_numeric(df_a['change'], errors='coerce')
    df_a['volume'] = pd.to_numeric(df_a['volume'], errors='coerce')

    # 强制将股票代码转换为字符串类型
    df_a['代码'] = df_a['代码'].astype(str).str.strip()

    # 打印数据（调试用）
    print("完整数据：")
    print(df_a.head())  # 打印前几行数据

    # 清理列名（去掉多余的空格）
    df_a.columns = df_a.columns.str.strip()

    # 检查 '代码' 列是否存在
    if '代码' not in df_a.columns:
        print("列 '代码' 不存在，请检查 CSV 文件。")
        return  # 退出程序

    # 打印所有股票代码，调试用
    print("所有股票代码：")
    print(df_a['代码'].unique())  # 打印所有唯一的股票代码

    # 4. 查询数据
    print("开始查询数据...")
    stock_code = input("请输入要查询的股票代码：").strip()  # 去除前后空格
    query_sqlite(f"SELECT * FROM a_stock WHERE code = '{stock_code}'")

    # 筛选数据并检查
    df_stock = df_a[df_a['代码'] == stock_code]  # 筛选指定股票的数据
    if df_stock.empty:
        print(f"没有找到股票代码 {stock_code} 的数据！")
        return  # 如果没有数据，退出程序

    print(f"筛选出的 {stock_code} 股票数据：")
    print(df_stock.head())  # 打印筛选后的数据

    # 5. 数据可视化
    print(f"开始可视化股票 {stock_code} 的数据...")
    plot_k_line(df_stock, stock_code)
    plot_volume_and_change(df_stock, stock_code)

# 执行主程序
if __name__ == "__main__":
    main()
