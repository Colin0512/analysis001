# This is the 'app.py' script
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import requests

# 文件路径设置
ROOT_DIR = r"D:\StockAnalysisProject"
DATA_DIR = os.path.join(ROOT_DIR, "data")
DB_FILE = os.path.join(DATA_DIR, "stock_data.db")
API_URL = "http://127.0.0.1:1234/v1/completions"  # LM Studio API 地址

# 数据库连接
def get_connection():
    """连接 SQLite 数据库"""
    try:
        return sqlite3.connect(DB_FILE)
    except Exception as e:
        st.error(f"数据库连接失败：{e}")
        return None

# 获取所有股票代码
def get_all_stock_codes(conn):
    """从数据库中获取所有股票代码"""
    try:
        query = "SELECT DISTINCT code FROM a_stock"
        return pd.read_sql_query(query, conn)['code'].tolist()
    except Exception as e:
        st.error(f"获取股票代码失败：{e}")
        return []

# 获取股票数据
def get_stock_data(conn, stock_code):
    """根据股票代码查询数据"""
    try:
        query = "SELECT * FROM a_stock WHERE code = ?"
        return pd.read_sql_query(query, conn, params=(stock_code,))
    except Exception as e:
        st.error(f"查询数据失败：{e}")
        return pd.DataFrame()

# 绘制趋势图
def plot_trends(df, stock_code):
    """绘制股票的价格和成交量趋势图"""
    try:
        fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        # 价格趋势
        axes[0].plot(df.index, df['price'], color='blue', marker='o', label='Price')
        axes[0].set_title(f"{stock_code} - Price Trend")
        axes[0].set_ylabel("Price")
        axes[0].legend()
        axes[0].grid()

        # 成交量趋势
        axes[1].bar(df.index, df['volume'], color='green', alpha=0.7, label='Volume')
        axes[1].set_title(f"{stock_code} - Volume Trend")
        axes[1].set_ylabel("Volume")
        axes[1].set_xlabel("Index")
        axes[1].legend()
        axes[1].grid()

        st.pyplot(fig)
    except Exception as e:
        st.error(f"绘图失败：{e}")

# 调用 AI 模型生成投资建议
def generate_ai_advice(stock_name, stock_code, open_price, close_price, volume):
    """
    调用 LM Studio 模型生成投资建议
    """
    prompt = f"""
    Analyze the stock {stock_name} ({stock_code}):
    - Open price: {open_price} USD
    - Close price: {close_price} USD
    - Volume: {volume:,}
    Provide investment suggestions (e.g., buy, sell, hold) and reasoning.
    """
    payload = {
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0].get('text', '').strip()
        else:
            st.error("AI 返回格式错误：未找到有效内容。")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"AI 请求失败：{e}")
        return None

# 主程序
def main():
    st.title("股票数据分析与投资建议")
    st.sidebar.header("股票查询工具")

    # 数据库连接
    conn = get_connection()
    if not conn:
        return

    # 获取所有股票代码
    stock_codes = get_all_stock_codes(conn)
    if not stock_codes:
        st.warning("数据库中没有可用的股票数据。")
        conn.close()
        return

    # 侧边栏选择股票代码
    stock_code = st.sidebar.selectbox("请选择股票代码", stock_codes)

    if stock_code:
        df = get_stock_data(conn, stock_code)
        if not df.empty:
            st.subheader(f"{stock_code} - 股票数据")
            st.dataframe(df)

            st.subheader("趋势图")
            plot_trends(df, stock_code)

            # 生成投资建议
            st.subheader("AI 投资建议")
            if st.button("生成投资建议"):
                # 提取最新数据
                try:
                    stock_name = stock_code  # 假设股票名称与代码相同
                    st.write(f"数据框列名: {df.columns.tolist()}")  # 打印列名以便检查

                    # 使用实际的列名，假设 'price' 列作为开盘和收盘价格
                    open_price = df['price'].iloc[0] if 'price' in df.columns else None  # 使用第一条记录的价格作为开盘价
                    close_price = df['price'].iloc[-1] if 'price' in df.columns else None  # 使用最后一条记录的价格作为收盘价
                    volume = df['volume'].iloc[-1] if 'volume' in df.columns else None

                    if open_price is not None and close_price is not None and volume is not None:
                        # 调用 AI 生成建议
                        advice = generate_ai_advice(stock_name, stock_code, open_price, close_price, volume)
                        if advice:
                            st.success("投资建议：")
                            st.write(advice)
                        else:
                            st.error("AI 无法生成有效的建议。")
                    else:
                        st.error("数据缺失，无法生成投资建议。")
                except IndexError:
                    st.error("数据不足，无法生成投资建议。")
        else:
            st.warning(f"未找到股票代码 {stock_code} 的数据。")

    # 关闭数据库连接
    conn.close()

if __name__ == "__main__":
    main()
