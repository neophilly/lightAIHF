# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import requests
import json
import time
from datetime import datetime
import logging
import re
from typing import Dict, Any, Optional
import random
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("stock_analyzer.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("data_fetcher")


class StockDataFetcher:
    def __init__(self, tushare_token: str = None):
        """初始化数据获取器

        Args:
            tushare_token: 可选的Tushare token，用于备用数据源
        """
        # 初始化请求头和会话
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.retry_count = 3

    def _make_request(self, url, params, timeout=5):
        """封装请求方法，增加重试机制"""
        for i in range(self.retry_count):
            try:
                response = self.session.get(url, params=params, headers=self.headers, timeout=timeout)
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                logging.warning(f"请求失败，重试第 {i + 1} 次: {str(e)}")
                time.sleep(2 ** i)  # 指数退避
        logging.error(f"请求失败，达到最大重试次数: {url}")
        return None

    def get_stock_info(self, code_or_name: str) -> Dict[str, Any]:
        """获取股票基本信息

        Args:
            code_or_name: 股票代码或名称

        Returns:
            包含股票基本信息的字典
        """
        try:
            # 格式化股票代码
            stock_code = self._format_stock_code(code_or_name)
            if not stock_code:
                logging.error(f"无效的股票代码或名称: {code_or_name}")
                return {}

            # 获取实时行情
            quotes = self._get_realtime_quotes(stock_code)
            if not quotes:
                return {}

            # 获取财务指标
            financial = self.get_financial_indicators(stock_code)

            # 合并数据
            stock_data = {
                "ts_code": stock_code,
                "name": quotes.get("name", ""),
                "price": quotes.get("price", 0.0),
                "change_percent": quotes.get("change_percent", 0.0),
                "pe_ttm": financial.get("pe_ttm", 0.0),
                "pb": financial.get("pb", 0.0),
                "total_shares": financial.get("total_share", 0.0),
                "float_shares": financial.get("float_share", 0.0),
                "total_assets": financial.get("total_assets", 0.0),
                "revenue": financial.get("revenue", 0.0),
                "net_profit": financial.get("net_profit", 0.0),
                "roe": financial.get("roe", 0.0),
                "debt_ratio": financial.get("debt_ratio", 0.0),
                "gross_margin": financial.get("gross_margin", 0.0),
                "dividend_yield": financial.get("dividend_yield", 0.0),
                "industry": financial.get("industry", ""),
            }

            return stock_data

        except Exception as e:
            logging.error(f"获取股票信息失败: {str(e)}")
            return {}

    def _format_stock_code(self, code: str) -> str:
        """格式化股票代码

        Args:
            code: 原始股票代码或名称

        Returns:
            格式化后的股票代码
        """
        # 去除空格和点
        code = code.strip().replace('.', '')

        # 如果已经有前缀，直接返回小写形式
        if code.lower().startswith(('sh', 'sz')):
            return code.lower()

        # 去除所有非数字字符
        code = ''.join(filter(str.isdigit, code))

        # 根据股票代码规则判断市场
        if len(code) != 6:
            raise ValueError("股票代码必须是6位数字")

        # 沪市规则：
        # - 600开头、601开头、603开头、605开头：主板
        # - 688开头：科创板
        # 深市规则：
        # - 000开头：主板
        # - 002开头：中小板
        # - 300开头：创业板
        # - 301开头：创业板
        if code.startswith(('600', '601', '603', '605', '688')):
            return f"sh{code}"
        elif code.startswith(('000', '002', '300', '301')):
            return f"sz{code}"
        else:
            raise ValueError("无效的股票代码")

    def _get_realtime_quotes(self, stock_code: str) -> Dict[str, Any]:
        """获取实时行情数据"""
        try:
            market = '1' if stock_code.startswith('sh') else '0'
            code = stock_code[2:]
            secid = f"{market}.{code}"

            url = "https://push2.eastmoney.com/api/qt/stock/get"
            params = {
                'secid': secid,
                'ut': 'fa5fd1943c7b386f17342da8645e8a2',
                'fields': 'f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f85'
            }

            data = self._make_request(url, params, timeout=5)
            if data is None or 'data' not in data:
                return {}

            quote_data = data['data']
            return {
                'name': quote_data.get('f58', ''),  # 股票名称
                'price': quote_data.get('f43', 0),  # 最新价
                'change_amount': quote_data.get('f44', 0),  # 涨跌额
                'change_percent': quote_data.get('f45', 0),  # 涨跌幅
                'volume': quote_data.get('f47', 0),  # 成交量
                'amount': quote_data.get('f48', 0),  # 成交额
                'amplitude': quote_data.get('f49', 0),  # 振幅
                'high': quote_data.get('f44', 0),  # 最高
                'low': quote_data.get('f45', 0),  # 最低
                'open': quote_data.get('f46', 0),  # 开盘
                'prev_close': quote_data.get('f60', 0),  # 昨收
                'turnover': quote_data.get('f61', 0),  # 换手率
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except Exception as e:
            logging.error(f"获取实时行情失败: {str(e)}")
            return {}

    def get_financial_indicators(self, stock_code: str) -> Dict[str, Any]:
        """获取财务指标数据"""
        try:
            code = stock_code[2:] if stock_code.startswith(("sh", "sz")) else stock_code
            url = f"https://datacenter-web.eastmoney.com/api/data/v1/get"
            params = {
                'sortColumns': 'REPORT_DATE',
                'sortTypes': '-1',
                'pageSize': '1',
                'pageNumber': '1',
                'reportName': 'RPT_LICO_FIN_INDIC',
                'columns': 'ALL',
                'filter': f"(SECURITY_CODE='{code}')"
            }

            data = self._make_request(url, params, timeout=10)
            if data is None or not data.get("result") or not data["result"].get("data"):
                logging.warning(f"未找到{stock_code}的财务指标数据")
                return {}

            financial_data = data["result"]["data"][0]
            return {
                "pe_ttm": float(financial_data.get("PE_TTM", 0)),
                "pb": float(financial_data.get("PB", 0)),
                "roe": float(financial_data.get("ROE_WEIGHT", 0)),
                "debt_ratio": float(financial_data.get("DEBT_ASSET_RATIO", 0)),
                "gross_margin": float(financial_data.get("GROSS_PROFIT_RATIO", 0)),
                "net_profit_margin": float(financial_data.get("NETPROFIT_MARGIN", 0)),
                "total_assets": float(financial_data.get("TOT_ASSETS", 0)),
                "revenue": float(financial_data.get("OPERATE_INCOME", 0)),
                "net_profit": float(financial_data.get("NET_PROFIT_PARENT_COMP", 0)),
                "total_share": float(financial_data.get("TOT_SHARE", 0)),
                "float_share": float(financial_data.get("FLOAT_SHARE", 0)),
                "dividend_yield": float(financial_data.get("DVD_YIELD", 0)),
                "industry": financial_data.get("INDUSTRY", ""),
            }

        except Exception as e:
            logging.error(f"获取财务指标失败: {str(e)}")
            return {}

    def get_technical_indicators(self, stock_code: str) -> Dict[str, Any]:
        """获取技术指标数据"""
        try:
            # 获取K线数据
            df = self._get_kline_data(stock_code, period='daily', limit=200)
            if df is None or len(df) < 20:  # 确保有足够的数据计算指标
                return {}

            # 计算技术指标
            indicators = {}

            # 计算MACD
            exp1 = df['close'].ewm(span=12, adjust=False).mean()
            exp2 = df['close'].ewm(span=26, adjust=False).mean()
            df['MACD_DIF'] = exp1 - exp2
            df['MACD_DEA'] = df['MACD_DIF'].ewm(span=9, adjust=False).mean()
            df['MACD'] = (df['MACD_DIF'] - df['MACD_DEA']) * 2

            # 计算KDJ
            low_9 = df['low'].rolling(window=9).min()
            high_9 = df['high'].rolling(window=9).max()
            df['RSV'] = (df['close'] - low_9) / (high_9 - low_9) * 100
            df['K'] = df['RSV'].ewm(com=2).mean()
            df['D'] = df['K'].ewm(com=2).mean()
            df['J'] = 3 * df['K'] - 2 * df['D']

            # 计算RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))

            # 获取最新的技术指标
            latest = df.iloc[-1]
            indicators = {
                'MACD': {
                    'DIF': round(latest['MACD_DIF'], 3),
                    'DEA': round(latest['MACD_DEA'], 3),
                    'MACD': round(latest['MACD'], 3),
                    'trend': '金叉' if latest['MACD'] > 0 and df.iloc[-2]['MACD'] < 0 else
                             '死叉' if latest['MACD'] < 0 and df.iloc[-2]['MACD'] > 0 else
                             '上升' if latest['MACD'] > 0 else '下降'
                },
                'KDJ': {
                    'K': round(latest['K'], 2),
                    'D': round(latest['D'], 2),
                    'J': round(latest['J'], 2),
                    'trend': '超买' if latest['J'] > 80 else '超卖' if latest['J'] < 20 else '中性'
                },
                'RSI': {
                    'RSI': round(latest['RSI'], 2),
                    'trend': '超买' if latest['RSI'] > 70 else '超卖' if latest['RSI'] < 30 else '中性'
                },
                'price_data': {
                    'current': latest['close'],
                    'change_percent': latest['change_percent'],
                    'amplitude': latest['amplitude'],
                    'volume': latest['volume'],
                    'turnover': latest['turnover']
                }
            }

            return indicators

        except Exception as e:
            logging.error(f"计算技术指标失败: {str(e)}")
            return {}

    def _get_kline_data(self, stock_code: str, period: str = 'daily', limit: int = 100) -> Optional[pd.DataFrame]:
        """获取K线数据"""
        try:
            market = '1' if stock_code.startswith('sh') else '0'
            code = stock_code[2:]
            secid = f"{market}.{code}"

            period_map = {'daily': '101', 'weekly': '102', 'monthly': '103'}
            klt = period_map.get(period, '101')

            url = f"https://push2his.eastmoney.com/api/qt/stock/kline/get"
            params = {
                'secid': secid,
                'ut': 'fa5fd1943c7b386f17342da8645e8a2',
                'fields1': 'f1,f2,f3,f4,f5,f6',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                'klt': klt,
                'fqt': '1',  # 1：前复权，2：后复权，0：不复权
                'end': '20500101',
                'lmt': limit,
            }

            data = self._make_request(url, params, timeout=10)
            if data is None or data['data'] is None or data['data']['klines'] is None:
                logging.warning(f"未获取到{stock_code}的K线数据")
                return None

            # 解析K线数据
            klines = []
            for line in data['data']['klines']:
                items = line.split(',')
                klines.append({
                    'date': items[0],
                    'open': float(items[1]),
                    'close': float(items[2]),
                    'high': float(items[3]),
                    'low': float(items[4]),
                    'volume': float(items[5]),
                    'amount': float(items[6]),
                    'amplitude': float(items[7]),
                    'change_percent': float(items[8]),
                    'change_amount': float(items[9]),
                    'turnover': float(items[10])
                })

            return pd.DataFrame(klines)

        except Exception as e:
            logging.error(f"获取K线数据失败: {str(e)}")
            return None