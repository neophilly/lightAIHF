# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import investment_agents
from eastmoney_api import EastMoneyAPI
from ai_analyzer import AIAnalyzer
from typing import Dict, Any
import logging
import requests  # 用于捕获网络异常
import time
import sys
import io

# 最大重试次数
MAX_RETRIES = 3
# 重试间隔时间（秒）
RETRY_DELAY = 5
# 设置标准输出的编码为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    # 配置日志
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("初始化 EastMoneyAPI 实例")

    # 初始化东方财富数据获取器
    api = EastMoneyAPI()

    # 初始化分析器
    agents = {
        "1": investment_agents.QuantAgent(),
        "2": investment_agents.LynchAgent(),
        "3": investment_agents.ShortTermAgent(),
        "4": investment_agents.BuffettAgent(),
        "5": AIAnalyzer()  # AI分析器
    }

    print("\n欢迎使用股票分析系统 (使用东方财富API)")
    print("=" * 60)

    while True:
        code_or_name = input("\n请输入股票代码（如：300310或sh300310，输入q退出）：").strip()
        if code_or_name.lower() == "q":
            print("退出系统")
            break

        try:
            # 格式化股票代码
            if code_or_name.isdigit():
                if code_or_name.startswith(('600', '601', '603', '605', '688')):
                    stock_code = f"sh{code_or_name}"
                elif code_or_name.startswith(('000', '002', '300', '301')):
                    stock_code = f"sz{code_or_name}"
                else:
                    print("无效的股票代码")
                    continue
            else:
                stock_code = code_or_name

            # 获取实时行情数据
            print("\n正在获取股票数据...")
            quotes = fetch_data_with_retry(api.get_realtime_quotes, stock_code)
            if not quotes:
                print("获取股票数据失败，请检查代码是否正确或网络是否畅通")
                continue

            # 构建股票基本数据
            stock_data = {
                "ts_code": stock_code,
                "name": quotes.get("name", stock_code),
                "price": quotes.get("price", 0.0),
                "change_percent": quotes.get("change_percent", 0.0),
                # 添加默认值，以避免分析错误
                "pe_ttm": 0.0,
                "pb": 0.0,
                "roe": 0.0,
                "debt_ratio": 0.0,
                "gross_margin": 0.0,
                "net_profit_margin": 0.0,
                "total_assets": 0.0,
                "revenue": 0.0,
                "net_profit": 0.0,
                "total_share": 0.0,
                "float_share": 0.0,
                "total_shares": 0.0,  # 添加 total_shares 字段给 Buffett 分析使用
                "float_shares": 0.0,  # 添加 float_shares 字段给 Buffett 分析使用
                "dividend_yield": 0.0,
                "industry": "未知",
            }

            # 获取财务指标
            print("正在获取财务指标...")
            financial = fetch_data_with_retry(api.get_financial_indicators, stock_code)
            if financial:
                stock_data.update(financial)
                # 确保字段名称一致性
                if "total_share" in financial and "total_shares" not in financial:
                    stock_data["total_shares"] = financial["total_share"]
                if "float_share" in financial and "float_shares" not in financial:
                    stock_data["float_shares"] = financial["float_share"]
            else:
                print("未获取到财务指标数据，使用默认值进行分析")

            # 显示基本信息
            print("\n" + "-" * 60)
            print(f"股票代码：{stock_data['ts_code']}")
            print(f"股票名称：{stock_data['name']}")
            print(f"当前价格：{stock_data['price']:.2f} 元")

            # 根据涨跌幅显示不同颜色
            change_text = f"涨跌幅：{stock_data['change_percent']:.2f}%"
            if stock_data['change_percent'] > 0:
                print(f"{change_text} 📈")
            elif stock_data['change_percent'] < 0:
                print(f"{change_text} 📉")
            else:
                print(f"{change_text} ➖")

            print(f"市盈率(TTM)：{stock_data['pe_ttm']:.2f}")
            print(f"市净率：{stock_data['pb']:.2f}")
            print(f"ROE：{stock_data['roe']:.2f}%")  # 添加ROE显示
            print(f"所属行业：{stock_data['industry']}")
            print("-" * 60)

            # 获取技术指标
            print("\n正在获取技术指标...")
            tech_data = fetch_data_with_retry(api.get_technical_indicators, stock_code)
            if tech_data:
                print("\n" + "="*20 + " 技术指标分析 " + "="*20)

                # 显示MACD指标
                if 'MACD' in tech_data:
                    macd = tech_data['MACD']
                    print("\n【MACD指标】")
                    print(f"  趋势判断: {macd['trend']}")
                    print(f"  DIF线: {macd['DIF']:.3f}")
                    print(f"  DEA线: {macd['DEA']:.3f}")
                    print(f"  MACD值: {macd['MACD']:.3f}")

                # 显示KDJ指标
                if 'KDJ' in tech_data:
                    kdj = tech_data['KDJ']
                    print("\n【KDJ指标】")
                    print(f"  趋势判断: {kdj['trend']}")
                    print(f"  K值: {kdj['K']:.2f}")
                    print(f"  D值: {kdj['D']:.2f}")
                    print(f"  J值: {kdj['J']:.2f}")

                # 显示RSI指标
                if 'RSI' in tech_data:
                    rsi = tech_data['RSI']
                    print("\n【RSI指标】")
                    print(f"  趋势判断: {rsi['trend']}")
                    print(f"  RSI值: {rsi['RSI']:.2f}")

                # 显示BOLL指标 - 新添加
                if 'BOLL' in tech_data:
                    boll = tech_data['BOLL']
                    print("\n【BOLL指标】")
                    print(f"  趋势判断: {boll['trend']}")
                    print(f"  上轨: {boll['UPPER']:.2f}")
                    print(f"  中轨: {boll['MID']:.2f}")
                    print(f"  下轨: {boll['LOWER']:.2f}")

                # 显示移动平均线 - 新添加
                if 'MA' in tech_data:
                    ma = tech_data['MA']
                    print("\n【移动平均线】")
                    print(f"  趋势判断: {ma['trend']}")
                    print(f"  MA5: {ma['MA5']:.2f}")
                    print(f"  MA10: {ma['MA10']:.2f}")
                    print(f"  MA30: {ma['MA30']:.2f}")
                    print(f"  MA60: {ma['MA60']:.2f}")

                # 显示量价关系
                if 'price_data' in tech_data:
                    price = tech_data['price_data']
                    print("\n【量价信息】")
                    print(f"  成交量: {price['volume']:,.0f}手")
                    print(f"  换手率: {price['turnover']:.2f}%")
                    print(f"  振幅: {price['amplitude']:.2f}%")

                # 技术综合判断 - 新添加
                print("\n【技术综合判断】")
                tech_signals = []
                if 'MACD' in tech_data and tech_data['MACD']['trend'] in ['金叉', '上升']:
                    tech_signals.append("MACD多头信号")
                if 'KDJ' in tech_data:
                    if tech_data['KDJ']['trend'] == '超卖':
                        tech_signals.append("KDJ超卖反弹信号")
                    elif tech_data['KDJ']['trend'] == '超买':
                        tech_signals.append("KDJ超买回调信号")
                if 'RSI' in tech_data:
                    if tech_data['RSI']['trend'] == '超卖':
                        tech_signals.append("RSI超卖反弹信号")
                    elif tech_data['RSI']['trend'] == '超买':
                        tech_signals.append("RSI超买回调信号")
                if 'BOLL' in tech_data:
                    if tech_data['BOLL']['trend'] == '突破上轨':
                        tech_signals.append("BOLL突破上轨-强势信号")
                    elif tech_data['BOLL']['trend'] == '突破下轨':
                        tech_signals.append("BOLL突破下轨-反弹信号")

                if tech_signals:
                    print("  " + ", ".join(tech_signals))
                else:
                    print("  暂无明确信号，可能处于盘整阶段")

                print("="*50)

                # 更新股票数据，用于后续分析
                stock_data.update(tech_data)
            else:
                print("获取技术指标失败，将使用有限数据进行分析")

            # 用户选择分析方法
            print("\n请选择分析类型：")
            print("1. 量化交易分析")
            print("2. 彼得林奇分析")
            print("3. 短期交易分析")
            print("4. 巴菲特价值投资分析")
            print("5. AI智能分析")
            choice = input("请输入选择（默认1）: ").strip() or "1"

            try:
                if choice == "5":
                    # AI分析
                    print("\n正在进行AI分析，请稍候...")
                    report = agents[choice].analyze_stock(stock_data)
                    print("\n" + "-" * 50)
                    print("AI智能分析报告")
                    print("-" * 50)
                    print(report if report else "AI分析生成失败，请检查Ollama服务是否运行")
                else:
                    # 传统分析方法
                    report = agents[choice].analyze(stock_data)
                    print("\n" + "-" * 50)
                    print(f"{agents[choice].strategy.upper()} 分析报告")
                    print("-" * 50)
                    print(report)

            except Exception as e:
                print(f"分析过程中出现错误: {str(e)}")
                continue

        except ValueError as e:
            print(f"输入错误: {str(e)}")
            continue
        except Exception as e:
            print(f"发生错误: {str(e)}")
            continue

def fetch_data_with_retry(func, *args):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            data = func(*args)
            return data
        except requests.RequestException as e:
            logging.error(f"网络请求出错: {str(e)}, 第 {retries + 1} 次重试...")
            retries += 1
            time.sleep(RETRY_DELAY)
        except Exception as e:
            logging.error(f"数据获取出错: {str(e)}")
            break
    return None

if __name__ == "__main__":
    main()