# This is the 'get_stock_data.py' script
import akshare as ak
import pandas as pd
import os


# 获取 A 股实时行情
print("正在获取 A 股实时数据...")
try:
    df_a = ak.stock_zh_a_spot_em()  # 获取 A 股实时数据
    print("成功获取 A 股数据！")
except Exception as e:
    print(f"获取 A 股数据失败，错误信息：{e}")
    exit()

# 选择重要字段
print("正在选择字段...")
try:
    df_a = df_a[['代码', '名称', '最新价', '涨跌幅', '成交量', '成交额']]
    print("字段选择完成")
except Exception as e:
    print(f"选择字段失败，错误信息：{e}")
    exit()

# 数据处理
print("正在处理数据...")
try:
    df_a = df_a.rename(columns={'最新价': 'price', '涨跌幅': 'change', '成交量': 'volume', '成交额': 'turnover'})
    df_a['change'] = df_a['change'].astype(str)  # 确保为字符串
    df_a['change'] = df_a['change'].str.replace('%', '').astype(float)  # 去掉 % 并转换为浮点型
    print("数据处理完成")
except Exception as e:
    print(f"数据处理失败，错误信息：{e}")
    exit()

# 打印前 5 行
print("数据预览：")
try:
    print(df_a.head())
except Exception as e:
    print(f"数据预览失败，错误信息：{e}")
    exit()

# 保存为 CSV 文件
print("正在保存数据到 CSV 文件...")
try:
    df_a.to_csv("a_stock_data.csv", index=False, encoding="utf-8-sig")
    print("A 股数据已保存为 a_stock_data.csv")
except Exception as e:
    print(f"保存数据失败，错误信息：{e}")
    exit()

# 让用户输入保存路径
save_path = input("请输入 CSV 文件的保存路径（例如：C:\\Users\\Administrator\\Desktop）：")

# 拼接文件名
csv_file = os.path.join(save_path, "a_stock_data.csv")

# 保存 CSV 文件
df_a.to_csv(csv_file, index=False, encoding="utf-8-sig")
print(f"A 股数据已保存到：{csv_file}")
