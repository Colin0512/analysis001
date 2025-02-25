# This is the 'ai_analysis.py' script
import requests
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# LM Studio API 地址
API_URL = "http://127.0.0.1:1234/v1/completions"

def send_request_to_model(prompt, temperature=0.7, max_tokens=20000):
    """
    发送请求到 LM Studio API，获取模型分析结果。
    :param prompt: 提供给模型的文本提示
    :param temperature: 温度（影响模型输出的随机性）
    :param max_tokens: 输出最大字符数
    :return: 模型返回的分析结果
    """
    payload = {
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        # 检查 API 服务是否运行
        response = requests.get("http://127.0.0.1:1234/health", timeout=5)
        if response.status_code != 200:
            logging.error("LM Studio API 服务未就绪，请检查服务状态。")
            return None

        # 发送请求
        response = requests.post(API_URL, json=payload, timeout=60)  # 超时设置为60秒
        response.raise_for_status()  # 如果响应状态码为 4xx 或 5xx，抛出异常
        result = response.json()

        if 'choices' in result:
            return result['choices'][0].get('text', '').strip()
        else:
            logging.error("API 返回格式错误: 'choices' 键缺失")
            return None
    except requests.exceptions.Timeout:
        logging.error("请求超时，请检查服务器状态或增加超时时间。")
    except requests.exceptions.ConnectionError:
        logging.error("无法连接到 LM Studio API，请确认服务是否已启动。")
    except requests.exceptions.RequestException as e:
        logging.error(f"请求失败: {e}")
    except ValueError:
        logging.error("解析响应失败，无法处理返回的 JSON 数据。")
    return None


def analyze_stock(stock_code, stock_name, open_price, close_price, volume):
    """
    调用 LM Studio 模型分析股票数据，生成投资建议
    :param stock_code: 股票代码
    :param stock_name: 股票名称
    :param open_price: 开盘价
    :param close_price: 收盘价
    :param volume: 成交量
    :return: 模型生成的分析结果
    """
    # 构造 Prompt
    prompt = f"""
    Analyze the stock {stock_name} ({stock_code}):
    - Open price: {open_price} USD
    - Close price: {close_price} USD
    - Volume: {volume:,}
    Provide investment suggestions (e.g., buy, sell, hold) and reasoning.
    """

    # 发送请求并获取分析结果
    analysis_result = send_request_to_model(prompt)

    return analysis_result


if __name__ == "__main__":
    # 测试调用
    stock_code = "600519"  # 茅台股票代码
    stock_name = "Kweichow Moutai"
    open_price = 1800.50
    close_price = 1825.75
    volume = 320000

    # 获取投资建议
    analysis_result = analyze_stock(stock_code, stock_name, open_price, close_price, volume)
    
    if analysis_result:
        print("投资建议：", analysis_result)
    else:
        print("无法生成投资建议。")