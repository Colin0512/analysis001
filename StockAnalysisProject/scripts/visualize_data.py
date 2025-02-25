# This is the 'visualize_data.py' script
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os

def plot_k_line(stock_data, stock_code):
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data["price"], label="价格", color="blue", marker="o")
    plt.title(f"{stock_code} 股票价格走势")
    plt.xlabel("记录序号")
    plt.ylabel("价格")
    plt.legend()
    plt.grid()
    plt.show()

def plot_volume_and_change(stock_data, stock_code):
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(stock_data.index, stock_data["volume"], label="成交量", color="grey", alpha=0.6)
    ax1.set_xlabel("记录序号")
    ax1.set_ylabel("成交量", color="grey")
    ax1.tick_params(axis="y", labelcolor="grey")

    ax2 = ax1.twinx()
    ax2.plot(stock_data.index, stock_data["change"], label="涨跌幅", color="green", marker="o")
    ax2.set_ylabel("涨跌幅（%）", color="green")
    ax2.tick_params(axis="y", labelcolor="green")
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda temp, pos: f"{temp:.2f}%"))
    ax2.set_ylim(-10, 10)

    plt.title(f"{stock_code} 成交量和涨跌幅趋势图")
    fig.tight_layout()
    plt.grid()
    plt.show()
