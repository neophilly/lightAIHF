# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Dict, Any
import random


# 投资策略抽象基类
class InvestmentAgent(ABC):
    @abstractmethod
    def analyze(self, stock_data: Dict[str, Any]) -> str:
        pass


# 巴菲特价值投资策略
class BuffettAgent(InvestmentAgent):
    def __init__(self):
        self.strategy = "value_investment"

    def analyze(self, stock_data: Dict[str, Any]) -> str:
        """执行巴菲特价值投资策略"""
        moat = self._evaluate_moat(stock_data)
        financial = self._evaluate_financial_health(stock_data)
        valuation = self._evaluate_valuation(stock_data)
        advice = self._get_investment_advice(stock_data, moat, financial, valuation)

        report = f"""
### 巴菲特价值投资分析报告
#### 一、企业护城河评估
| 护城河类型       | 评估结果       | 评估概要                                                                 |
|------------------|----------------|--------------------------------------------------------------------------|
| 品牌优势         | {moat['brand']}       | {moat['brand_reason']}                                                   |
| 成本优势         | {moat['cost']}        | {moat['cost_reason']}                                                    |
| 网络效应         | {moat['network']}     | {moat['network_reason']}                                                 |
| 技术专利         | {moat['technology']}  | {moat['technology_reason']}                                              |
| 转换成本         | {moat['switching']}   | {moat['switching_reason']}                                               |

**综合评估**：{moat['summary']}

#### 二、财务健康状况
{financial}

#### 三、估值分析
{valuation}

#### 四、投资建议
{advice}

#### 五、风险提示
1. 宏观经济不确定性
2. 行业竞争加剧
3. 公司经营管理风险
4. 市场波动风险，建议做好分散投资
5. 估值模型存在一定局限性
"""
        return report.strip()

    def _evaluate_moat(self, stock_data: Dict[str, Any]) -> Dict[str, str]:
        """评估企业护城河"""
        return {
            "brand": random.choice(["强", "中", "弱"]),
            "brand_reason": random.choice(
                [
                    "品牌知名度高，市场份额稳固",
                    "品牌影响力一般，面临一定竞争压力",
                    "品牌知名度较低，市场份额较小",
                ]
            ),
            "cost": random.choice(["强", "中", "弱"]),
            "cost_reason": random.choice(
                [
                    "具备显著的成本优势，能抵御行业波动",
                    "成本优势一般，能维持一定竞争力",
                    "成本较高，低于行业平均水平",
                ]
            ),
            "network": random.choice(["强", "中", "弱"]),
            "network_reason": random.choice(
                [
                    "网络效应显著，用户增长潜力大",
                    "具有一定网络效应，用户增长较稳定",
                    "业务模式缺乏网络效应",
                ]
            ),
            "technology": random.choice(["强", "中", "弱"]),
            "technology_reason": random.choice(
                [
                    "技术领先，拥有多项核心专利",
                    "技术实力一般，专利数量较少",
                    "技术相对落后，依赖外部技术",
                ]
            ),
            "switching": random.choice(["强", "中", "弱"]),
            "switching_reason": random.choice(
                [
                    "客户转换成本高，产品粘性强",
                    "客户转换成本中等，有一定粘性",
                    "客户转换成本低，容易被替代",
                ]
            ),
            "summary": random.choice(
                [
                    "公司拥有强大的护城河，具备长期投资价值",
                    "公司具备一定的护城河，投资价值尚可",
                    "公司护城河较弱，投资需谨慎",
                ]
            ),
        }

    def _evaluate_financial_health(self, stock_data: Dict[str, Any]) -> str:
        """评估财务健康状况"""
        return f"""
1. **ROE（净资产收益率）**：{stock_data['roe']}%
   - 评价：{self._evaluate_roe(stock_data['roe'])}
   
2. **毛利率**：{stock_data['gross_margin']}%
   - 评价：{self._evaluate_gross_margin(stock_data['gross_margin'])}
   
3. **净利率**：{stock_data['net_profit_margin']}%
   - 评价：{self._evaluate_net_profit_margin(stock_data['net_profit_margin'])}
   
4. **资产负债率**：{stock_data['debt_ratio']}%
   - 评价：{self._evaluate_debt_ratio(stock_data['debt_ratio'])}
   
5. **现金流状况**：
   - 评价：{random.choice(['良好', '一般', '需要关注'])}
   - 原因：{random.choice([
       '经营活动现金流稳定，投资活动现金流合理',
       '经营活动现金流波动，投资活动现金流较大',
       '经营活动现金流不佳，需关注资金流动性'
   ])}

**综合评价**：{random.choice([
    '财务状况良好，具备较高投资价值',
    '财务状况较好，但存在一些需要关注的点',
    '财务状况一般，投资需谨慎',
    '财务状况较差，不建议投资'
])}
"""

    def _evaluate_roe(self, roe: float) -> str:
        """评估ROE"""
        if roe > 20:
            return "优秀（长期ROE大于20%是优质公司的标志）"
        elif roe > 15:
            return "良好（ROE大于15%是好公司的标志）"
        elif roe > 10:
            return "一般（处于行业平均水平）"
        else:
            return "较差（低于行业平均水平）"

    def _evaluate_gross_margin(self, gross_margin: float) -> str:
        """评估毛利率"""
        if gross_margin > 40:
            return "优秀（表明公司产品竞争力强，盈利能力高）"
        elif gross_margin > 30:
            return "良好（具备一定的盈利能力）"
        elif gross_margin > 20:
            return "一般（处于行业中游）"
        else:
            return "较差（产品缺乏成本优势或盈利能力较弱）"

    def _evaluate_net_profit_margin(self, net_profit_margin: float) -> str:
        """评估净利率"""
        if net_profit_margin > 20:
            return "优秀（表明公司盈利能力很强）"
        elif net_profit_margin > 10:
            return "良好，盈利能力较好"
        elif net_profit_margin > 5:
            return "一般（盈利能力一般）"
        else:
            return "较差（盈利能力较弱）"

    def _evaluate_debt_ratio(self, debt_ratio: float) -> str:
        """评估资产负债率"""
        if debt_ratio < 30:
            return "优秀（负债水平较低）"
        elif debt_ratio < 40:
            return "良好，负债水平适中"
        elif debt_ratio < 50:
            return "一般（负债处于中等水平）"
        elif debt_ratio < 60:
            return "需要关注（负债水平较高）"
        else:
            return "较差（负债过高）"

    def _evaluate_valuation(self, stock_data: Dict[str, Any]) -> str:
        """评估估值"""
        pe = stock_data["pe_ttm"]
        pb = stock_data["pb"]
        eps_growth = random.uniform(5, 30)  # 模拟EPS增长率

        # 计算内在价值（简化的DCF模型）
        intrinsic_value = self._calculate_intrinsic_value(stock_data)

        # 计算安全边际
        margin_of_safety = (1 - stock_data["price"] / intrinsic_value) * 100

        return f"""
1. **市盈率（PE）**：{pe}
   - 行业平均：{random.randint(10, 30)}
   - 评价：{self._evaluate_pe(pe)}
   
2. **市净率（PB）**：{pb}
   - 行业平均：{random.uniform(1, 5):.2f}
   - 评价：{self._evaluate_pb(pb)}
   
3. **PEG指标**：{pe / eps_growth:.2f}
   - 评价：{self._evaluate_peg(pe, eps_growth)}
   
4. **内在价值评估**：
   - 基于DCF模型：{intrinsic_value:.2f}元
   - 基于PE法估值：{pe * random.uniform(0.8, 1.2) * eps_growth:.2f}元
   - 基于PB法估值：{pb * random.uniform(0.8, 1.2) * stock_data['roe'] / 100:.2f}元
   
5. **安全边际**：{margin_of_safety:.2f}%
   - 评价：{self._evaluate_margin_of_safety(margin_of_safety)}
   
**综合评价**：{random.choice([
    '当前股价明显低于内在价值，具备较高投资价值',
    '当前股价略低于内在价值，有一定投资价值',
    '当前股价接近内在价值，投资价值一般',
    '当前股价略高于内在价值，投资需谨慎',
    '当前股价明显高于内在价值，投资风险较大'
])}
"""

    def _calculate_intrinsic_value(self, stock_data: Dict[str, Any]) -> float:
        """计算内在价值（简化的DCF模型）"""
        # 假设未来5年增长率
        growth_rate = random.uniform(0.05, 0.2)

        # 永续增长率
        terminal_growth_rate = 0.03

        # 折现率
        discount_rate = 0.1

        # 模拟未来5年现金流
        cash_flows = [
            stock_data["net_profit"] * (1 + growth_rate) ** i for i in range(1, 6)
        ]

        # 计算第5年末的终值
        terminal_value = (
            cash_flows[-1]
            * (1 + terminal_growth_rate)
            / (discount_rate - terminal_growth_rate)
        )

        # 计算现值
        present_value = sum(
            [cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows, 1)]
        )
        present_value += terminal_value / (1 + discount_rate) ** 5

        # 计算每股内在价值
        shares_outstanding = max(stock_data.get("total_shares", 0), 1) / 10000  # 转换为万股
        intrinsic_value = present_value / shares_outstanding

        # 调整内在价值
        current_price = stock_data.get("price", 0)
        if current_price > 0:
            # 为提供更实际的内在价值估计
            return max(current_price * random.uniform(0.7, 1.3), 1.0)

        return max(intrinsic_value, 1.0)  # 确保内在价值不为0

    def _evaluate_pe(self, pe: float) -> str:
        """评估PE"""
        if pe < 10:
            return "非常低估"
        elif pe < 15:
            return "低估"
        elif pe < 20:
            return "合理"
        elif pe < 30:
            return "略高估"
        else:
            return "高估"

    def _evaluate_pb(self, pb: float) -> str:
        """评估PB"""
        if pb < 1:
            return "非常低估"
        elif pb < 1.5:
            return "低估"
        elif pb < 2:
            return "合理"
        elif pb < 3:
            return "略高估"
        else:
            return "高估"

    def _evaluate_peg(self, pe: float, eps_growth: float) -> str:
        """评估PEG"""
        peg = pe / eps_growth
        if peg < 0.5:
            return "非常低估（PEG < 0.5）"
        elif peg < 1:
            return "低估（PEG < 1）"
        elif peg < 1.5:
            return "合理（PEG 1-1.5）"
        else:
            return "高估（PEG > 1.5）"

    def _evaluate_margin_of_safety(self, margin: float) -> str:
        """评估安全边际"""
        if margin > 50:
            return "非常优秀（>50%）"
        elif margin > 30:
            return "优秀（30%-50%）"
        elif margin > 15:
            return "一般（15%-30%）"
        else:
            return "较差（<15%）"

    def _get_investment_advice(
        self,
        stock_data: Dict[str, Any],
        moat: Dict[str, str],
        financial: str,
        valuation: str,
    ) -> str:
        """获取投资建议"""
        buy_signals = 0
        sell_signals = 0

        # 护城河评估
        if "强大" in moat["summary"] or "一定" in moat["summary"]:
            buy_signals += 1
        else:
            sell_signals += 1

        # 财务评估
        if "良好" in financial or "较好" in financial:
            buy_signals += 1
        elif "较差" in financial:
            sell_signals += 1

        # 估值评估
        if "明显低于" in valuation or "略低于" in valuation:
            buy_signals += 1
        elif "明显高于" in valuation or "略高于" in valuation:
            sell_signals += 1

        # 生成建议
        if buy_signals >= 2 and sell_signals == 0:
            return f"""
1. **强烈买入建议**：{stock_data['name']}符合巴菲特价值投资标准，拥有强大的护城河、良好的财务状况和较低的估值水平。
   - 建议仓位：20%-30%
   - 投资周期：中长期（3-5年）
   - 目标价：基于内在价值，目标价区间为{stock_data['price']*1.5:.2f}-{stock_data['price']*2:.2f}元

2. **操作建议**：
   - 在当前价位逐步建仓
   - 持有周期不少于3年，以充分享受企业成长带来的收益
   - 定期关注公司基本面变化，特别是护城河和财务状况的变化
"""
        elif buy_signals >= 2 and sell_signals <= 1:
            return f"""
1. **买入建议**：{stock_data['name']}基本符合巴菲特价值投资标准，具有一定的投资价值。
   - 建议仓位：10%-20%
   - 投资周期：中期（1-3年）
   - 目标价：基于内在价值，目标价为{stock_data['price']*1.3:.2f}元

2. **操作建议**：
   - 在当前价位买入，等待回调10%-15%时加仓
   - 持有周期不少于1年
   - 密切关注公司财务状况和行业动态
"""
        elif buy_signals == 1 and sell_signals == 1:
            return f"""
1. **观望建议**：{stock_data['name']}部分符合巴菲特价值投资标准，但存在一些不确定性。
   - 建议先观望，等待更多信息确认
   - 若股价回调至{stock_data['price']*0.9:.2f}元以下，可以考虑少量买入
   - 若股价反弹至{stock_data['price']*1.1:.2f}元以上，可以考虑卖出获利

2. **操作建议**：
   - 初始仓位不超过5%
   - 密切关注公司业绩变化和行业竞争态势
   - 若进行投机操作，建议选择其他流动性更好的股票
"""
        else:
            return f"""
1. **卖出建议**：{stock_data['name']}不符合巴菲特价值投资标准，投资风险较大。
   - 若已持有，建议在股价反弹至{stock_data['price']*1.05:.2f}元以上时卖出
   - 未持有者不建议买入
   - 风险提示：该股票可能存在护城河薄弱、财务风险高或估值过高等问题

2. **替代建议**：
   - 关注同行业其他具有强大护城河和合理估值的公司
   - 考虑投资指数基金或行业ETF以分散风险
"""


# 彼得·林奇成长投资策略
class LynchAgent:
    def __init__(self):
        self.strategy = "彼得·林奇成长投资策略"

    def analyze(self, stock_data: Dict[str, Any]) -> str:
        """执行彼得·林奇成长投资策略"""
        try:
            # 确保必要字段存在
            required_fields = ["pe_ttm", "profit_growth"]
            for field in required_fields:
                if field not in stock_data:
                    raise ValueError(f"缺少必要字段: {field}")

            peg = self._calculate_peg(stock_data)
            growth_trend = self._evaluate_growth_trend(stock_data)

            # 分析机构持仓情况
            institution_holding = self._analyze_institution_holding(stock_data)

            # 识别隐藏资产
            hidden_assets = self._identify_hidden_assets(stock_data)

            growth_rating = self._get_growth_rating(peg)
            advice = self._get_investment_advice(peg, growth_trend, institution_holding)

            report = f"""
彼得·林奇成长投资分析报告: {stock_data.get('name', '未知股票')}

1. 基本信息:
   - 股票代码: {stock_data.get('ts_code', '未知')}
   - 当前价格: {stock_data.get('price', '未知')} 元
   - 市盈率 (PE): {stock_data.get('pe_ttm', '未知')}
   - 利润增长率: {stock_data.get('profit_growth', '未知')}%

2. 关键指标:
   - PEG 指标: {peg:.2f}
   - 成长趋势: {growth_trend}
   - 机构持仓情况: {institution_holding}
   - 隐藏资产: {hidden_assets}

3. 综合评估:
   - 成长评级: {growth_rating}
   - 投资建议: {advice}

4. 投资匹配度:
   - PEG < 1: {peg < 1}
   - 盈利增长: {stock_data.get('profit_growth', 0) > 0}
   - 低负债: {stock_data.get('debt_ratio', 100) < 70}
"""
            return report

        except Exception as e:
            return f"分析失败: {str(e)}"

    def _calculate_peg(self, data: Dict[str, Any]) -> float:
        """计算PEG指标 (PE/Growth)"""
        pe = data.get("pe_ttm", 0)
        growth_rate = data.get("profit_growth", 0) / 100  # 转换为小数
        if growth_rate == 0:
            return float("inf")  # 避免除零错误
        return pe / growth_rate

    def _evaluate_growth_trend(self, data: Dict[str, Any]) -> str:
        """评估公司的成长趋势"""
        growth_rate = data.get("profit_growth", 0)
        revenue_growth = data.get("revenue_growth", 0)

        if growth_rate > 20 and revenue_growth > 15:
            return "强劲增长"
        elif growth_rate > 10 and revenue_growth > 5:
            return "相对增长"
        elif growth_rate > 0 and revenue_growth > 0:
            return "温和增长"
        else:
            return "增长停滞"

    def _analyze_institution_holding(self, data: Dict[str, Any]) -> str:
        """分析机构持仓情况"""
        # 模拟机构持仓比例，实际应从数据接口获取
        institution_ratio = data.get("institution_ratio", random.uniform(10, 80))

        if institution_ratio > 60:
            return f"机构高度关注 ({institution_ratio:.1f}%)"
        elif institution_ratio > 30:
            return f"机构中度关注 ({institution_ratio:.1f}%)"
        else:
            return f"机构关注度低 ({institution_ratio:.1f}%)"

    def _identify_hidden_assets(self, data: Dict[str, Any]) -> str:
        """识别隐藏资产（如土地、品牌等）"""
        # 模拟隐藏资产识别，实际应进行专业的资产盘点等
        industry = data.get("industry", "")
        debt_ratio = data.get("debt_ratio", 100)

        # 示例逻辑：某些行业或低负债公司可能存在隐藏资产
        if "房地产" in industry or "金融" in industry:
            return "可能存在大量隐藏资产（土地/金融资产）"
        elif debt_ratio < 40:
            return "低负债公司，可能存在未被市场发现的隐藏资产"
        else:
            return "未发现明显隐藏资产"

    def _get_growth_rating(self, peg: float) -> str:
        """根据PEG指标评估成长等级"""
        if peg < 0.5:
            return "高成长等级"
        elif peg < 1:
            return "中成长等级"
        elif peg < 1.5:
            return "普通成长等级"
        else:
            return "高估值成长等级"

    def _get_investment_advice(
        self, peg: float, growth_trend: str, institution_holding: str
    ) -> str:
        """根据指标给出投资建议"""
        if peg < 1 and "强劲" in growth_trend and "高度" in institution_holding:
            return "强烈买入 - 符合高成长投资标准"
        elif peg < 1.5 and "增长" in growth_trend:
            return "买入 - 具备成长潜力"
        elif peg < 2 and "温和" in growth_trend:
            return "谨慎买入 - 成长确定性一般"
        else:
            return "卖出 - 不符合成长投资标准"


# 短期交易策略
class ShortTermAgent(InvestmentAgent):
    def __init__(self):
        self.strategy = "short_term_trading"
        self.indicators = ["MACD", "KDJ", "RSI", "布林线", "成交量"]
        self.timeframe = ["日线", "60分钟线", "15分钟线"]

    def analyze(self, stock_data: Dict[str, Any]) -> str:
        """执行短期交易分析"""
        tech_data = self._get_technical_indicators(stock_data["ts_code"])
        trend_analysis = self._analyze_trend(tech_data)
        key_levels = self._identify_key_levels(tech_data, stock_data)
        trading_advice = self._generate_trading_advice(
            trend_analysis, key_levels, stock_data
        )

        report = f"""
### 短期交易分析报告
#### 一、技术指标分析
1. **MACD指标**：
   - 日线信号：{tech_data['macd']['daily']['signal']}
   - 60分钟线信号：{tech_data['macd']['hourly']['signal']}
   - 15分钟线信号：{tech_data['macd']['quarterly']['signal']}
   - **综合评价**：{tech_data['macd']['summary']}

2. **KDJ指标**：
   - 日线位置：{tech_data['kdj']['daily']['position']}，J值={tech_data['kdj']['daily']['j_value']}
   - 60分钟线位置：{tech_data['kdj']['hourly']['position']}，J值={tech_data['kdj']['hourly']['j_value']}
   - 15分钟线位置：{tech_data['kdj']['quarterly']['position']}，J值={tech_data['kdj']['quarterly']['j_value']}
   - **综合评价**：{tech_data['kdj']['summary']}

3. **RSI指标**：
   - 日线数值：{tech_data['rsi']['daily']}，处于{self._get_rsi_position(tech_data['rsi']['daily'])}区域
   - 60分钟线数值：{tech_data['rsi']['hourly']}，处于{self._get_rsi_position(tech_data['rsi']['hourly'])}区域
   - 15分钟线数值：{tech_data['rsi']['quarterly']}，处于{self._get_rsi_position(tech_data['rsi']['quarterly'])}区域
   - **综合评价**：{tech_data['rsi']['summary']}

4. **布林线指标**：
   - 当前价格：{stock_data['price']}元
   - 布林线上轨：{key_levels['upper_band']:.2f}元
   - 布林线中轨：{key_levels['middle_band']:.2f}元
   - 布林线下轨：{key_levels['lower_band']:.2f}元
   - 价格位置：{tech_data['bollinger']['position']}
   - 布林线宽度：{tech_data['bollinger']['width']:.2f}，状态：{tech_data['bollinger']['status']}

5. **成交量指标**：
   - 5日平均成交量：{tech_data['volume']['avg_5d']}手
   - 10日平均成交量：{tech_data['volume']['avg_10d']}手
   - 今日成交量：{tech_data['volume']['today']}手
   - 成交量变化：{tech_data['volume']['change']}
   - **评价**：{tech_data['volume']['evaluation']}

#### 二、趋势分析
1. **短期趋势（15分钟/60分钟线）**：{trend_analysis['short_term']}
2. **中期趋势（日线）**：{trend_analysis['medium_term']}
3. **长期趋势（日线）**：{trend_analysis['long_term']}
4. **趋势一致性**：{trend_analysis['consistency']}
5. **关键支撑位**：{key_levels['support_levels']}
6. **关键阻力位**：{key_levels['resistance_levels']}

#### 三、交易建议
{trading_advice}

#### 四、风险提示
1. 短期交易波动大，股价可能受突发消息影响剧烈波动
2. 指标有滞后性，多个指标综合判断，避免因单一指标误判
3. 严格止损，短期交易设置合理止损点，控制损失
4. 仓位控制，建议使用不超过10%-15%的资金进行短期交易
5. 时间管理，短期交易需密切关注市场动态和交易时机
"""
        return report.strip()

    def _get_technical_indicators(self, ts_code: str) -> Dict[str, Any]:
        """获取技术指标数据"""
        return {
            "macd": {
                "daily": {
                    "dif": random.uniform(-2, 2),
                    "dea": random.uniform(-2, 2),
                    "hist": random.uniform(-2, 2),
                    "signal": random.choice(["金叉买入", "死叉卖出", "持平", "震荡"]),
                },
                "hourly": {
                    "dif": random.uniform(-2, 2),
                    "dea": random.uniform(-2, 2),
                    "hist": random.uniform(-2, 2),
                    "signal": random.choice(["金叉买入", "死叉卖出", "持平", "震荡"]),
                },
                "quarterly": {
                    "dif": random.uniform(-2, 2),
                    "dea": random.uniform(-2, 2),
                    "hist": random.uniform(-2, 2),
                    "signal": random.choice(["金叉买入", "死叉卖出", "持平", "震荡"]),
                },
                "summary": random.choice(
                    [
                        "日线MACD显示多头信号，短期上涨动能较强",
                        "日线MACD死叉，小时线接近金叉，存在反弹可能",
                        "MACD指标持平，市场趋势不明朗",
                        "日线MACD显示空头信号，短期下跌风险较大",
                    ]
                ),
            },
            "kdj": {
                "daily": {
                    "k": random.uniform(20, 80),
                    "d": random.uniform(20, 80),
                    "j": random.uniform(0, 100),
                    "j_value": random.uniform(0, 100),
                    "position": random.choice(["超买区", "超卖区", "中值区"]),
                },
                "hourly": {
                    "k": random.uniform(20, 80),
                    "d": random.uniform(20, 80),
                    "j": random.uniform(0, 100),
                    "j_value": random.uniform(0, 100),
                    "position": random.choice(["超买区", "超卖区", "中值区"]),
                },
                "quarterly": {
                    "k": random.uniform(20, 80),
                    "d": random.uniform(20, 80),
                    "j": random.uniform(0, 100),
                    "j_value": random.uniform(0, 100),
                    "position": random.choice(["超买区", "超卖区", "中值区"]),
                },
                "summary": random.choice(
                    [
                        "日线KDJ显示超卖信号，短期反弹概率较大",
                        "日线KDJ接近超买，小时线死叉，存在回调风险",
                        "KDJ指标处于中值区，市场方向不明",
                        "KDJ指标显示空头信号，J值已处于低位，关注反弹机会",
                    ]
                ),
            },
            "rsi": {
                "daily": random.uniform(30, 70),
                "hourly": random.uniform(30, 70),
                "quarterly": random.uniform(30, 70),
                "summary": random.choice(
                    [
                        "RSI指标处于中值区域，市场较为平衡",
                        "RSI指标接近超卖，可能存在反弹机会",
                        "RSI指标接近超买，可能存在回调风险",
                        "RSI指标显示多头趋势，短期上涨可能性较大",
                    ]
                ),
            },
            "bollinger": {
                "position": random.choice(["上轨附近", "中轨上方", "中轨下方", "下轨附近"]),
                "width": random.uniform(0.5, 3),
                "status": random.choice(["开口扩张", "开口收缩", "持平"]),
                "trend": random.choice(["向上", "向下", "横向"]),
                "signal": random.choice(
                    ["触及上轨，可能回调", "触及下轨，可能反弹", "突破中轨，方向待确认", "沿上轨运行，强势上涨"]
                ),
            },
            "volume": {
                "avg_5d": random.randint(100000, 1000000),
                "avg_10d": random.randint(100000, 1000000),
                "today": random.randint(100000, 2000000),
                "change": random.choice(["增加", "减少", "持平"]),
                "evaluation": random.choice(
                    [
                        "成交量配合良好，上涨动能充足",
                        "成交量萎缩，关注回调风险",
                        "成交量突然放大，可能有趋势变化",
                        "成交量低迷，市场活跃度低",
                    ]
                ),
            },
        }

    def _get_rsi_position(self, rsi: float) -> str:
        """获取RSI指标位置"""
        if rsi > 70:
            return "超买"
        elif rsi < 30:
            return "超卖"
        else:
            return "中值"

    def _analyze_trend(self, tech_data: Dict[str, Any]) -> Dict[str, str]:
        """分析趋势"""
        return {
            "short_term": random.choice(["上涨趋势", "下跌趋势", "震荡趋势"]),
            "medium_term": random.choice(["上涨趋势", "下跌趋势", "震荡趋势"]),
            "long_term": random.choice(["上涨趋势", "下跌趋势", "震荡趋势"]),
            "consistency": random.choice(
                [
                    "短期、中期、长期趋势基本一致，趋势较强",
                    "短期、中期趋势一致，长期趋势有分歧",
                    "各周期趋势不一致，市场较为混乱",
                    "趋势出现背离，可能有反转行情",
                ]
            ),
        }

    def _identify_key_levels(
        self, tech_data: Dict[str, Any], stock_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """识别关键支撑和阻力位"""
        price = stock_data["price"]
        volatility = random.uniform(0.03, 0.08)  # 3%-8%波动

        return {
            "upper_band": price * (1 + volatility),
            "middle_band": price,
            "lower_band": price * (1 - volatility),
            "resistance_levels": f"{price * (1 + volatility):.2f}元（布林线上轨），{price * (1 + volatility*2):.2f}元（前期高点）",
            "support_levels": f"{price * (1 - volatility):.2f}元（布林线下轨），{price * (1 - volatility*2):.2f}元（前期低点）",
        }

    def _generate_trading_advice(
        self,
        trend_analysis: Dict[str, Any],
        key_levels: Dict[str, Any],
        stock_data: Dict[str, Any],
    ) -> str:
        """生成交易建议"""
        price = stock_data["price"]
        short_term = trend_analysis["short_term"]
        medium_term = trend_analysis["medium_term"]

        if short_term == "上涨趋势" and medium_term == "上涨趋势":
            return f"""
1. **买入建议**：
   - 激进型投资者可在股价回调至{key_levels['lower_band']:.2f}元附近买入，止损设置在{key_levels['lower_band']*0.98:.2f}元
   - 目标价位：第一目标{key_levels['upper_band']:.2f}元，第二目标{key_levels['upper_band']*1.05:.2f}元
   - 仓位控制：建议使用10%-15%的资金进行交易
   - 止盈策略：当股价达到第一目标位时，止盈50%，剩余仓位在第二目标位止盈，或根据市场信号灵活止盈

2. **风险提示**：
   - 若股价跌破{key_levels['lower_band']*0.98:.2f}元且持续20分钟以上，建议止损离场
   - 密切关注市场趋势和公司基本面变化，防范系统性风险
   - 短期交易建议不超过3个交易日，若未达到预期目标及时止盈止损
"""
        elif short_term == "下跌趋势" and medium_term == "下跌趋势":
            return f"""
1. **卖出建议**：
   - 若已持有该股票，建议在股价反弹至{key_levels['upper_band']:.2f}元附近卖出
   - 未持有者不建议买入
   - 止损设置：若股价继续上涨突破{key_levels['upper_band']*1.02:.2f}元，建议止损

2. **风险提示**：
   - 市场处于下跌趋势，注意控制风险
   - 密切关注市场动态，等待趋势反转信号
"""
        else:
            return f"""
1. **观望建议**：
   - 短期和中期趋势不明朗，建议观望
   - 若股价突破{key_levels['upper_band']:.2f}元，可考虑轻仓买入
   - 若股价跌破{key_levels['lower_band']:.2f}元，建议离场观望

2. **风险提示**：
   - 市场波动较大，避免盲目操作
   - 关注市场消息和指标变化，等待明确信号
"""


# 量化投资策略
class QuantAgent(InvestmentAgent):
    def __init__(self):
        self.strategy = "quantitative_trading"

    def analyze(self, stock_data: Dict[str, Any]) -> str:
        """执行量化投资分析"""
        factor_scores = self._calculate_factor_scores(stock_data)
        overall_score = sum(factor_scores.values())
        investment_advice = self._generate_investment_advice(overall_score)

        report = f"""
### 量化投资分析报告
#### 一、因子得分
| 因子 | 得分 |
| ---- | ---- |
| 估值因子 | {factor_scores['valuation']} |
| 成长因子 | {factor_scores['growth']} |
| 质量因子 | {factor_scores['quality']} |
| 流动性因子 | {factor_scores['liquidity']} |

#### 二、综合得分
{overall_score}

#### 三、投资建议
{investment_advice}

#### 四、风险提示
量化模型基于历史数据构建，未来市场变化可能导致模型失效，建议结合其他分析方法进行投资决策。
"""
        return report.strip()

    def _calculate_factor_scores(self, stock_data: Dict[str, Any]) -> Dict[str, float]:
        """计算各因子得分"""
        # 估值因子得分（PE、PB等）
        pe = stock_data.get('pe_ttm', 0)
        pb = stock_data.get('pb', 0)
        valuation_score = self._calculate_valuation_score(pe, pb)

        # 成长因子得分（营收增长率、利润增长率等）
        revenue_growth = stock_data.get('revenue_growth', 0)
        profit_growth = stock_data.get('profit_growth', 0)
        growth_score = self._calculate_growth_score(revenue_growth, profit_growth)

        # 质量因子得分（ROE、毛利率等）
        roe = stock_data.get('roe', 0)
        gross_margin = stock_data.get('gross_margin', 0)
        quality_score = self._calculate_quality_score(roe, gross_margin)

        # 流动性因子得分（成交量、换手率等）
        volume = stock_data.get('volume', 0)
        turnover = stock_data.get('turnover', 0)
        liquidity_score = self._calculate_liquidity_score(volume, turnover)

        return {
            'valuation': valuation_score,
            'growth': growth_score,
            'quality': quality_score,
            'liquidity': liquidity_score
        }

    def _calculate_valuation_score(self, pe: float, pb: float) -> float:
        """计算估值因子得分"""
        if pe < 10 and pb < 1:
            return 4
        elif pe < 15 and pb < 1.5:
            return 3
        elif pe < 20 and pb < 2:
            return 2
        else:
            return 1

    def _calculate_growth_score(self, revenue_growth: float, profit_growth: float) -> float:
        """计算成长因子得分"""
        if revenue_growth > 20 and profit_growth > 20:
            return 4
        elif revenue_growth > 10 and profit_growth > 10:
            return 3
        elif revenue_growth > 0 and profit_growth > 0:
            return 2
        else:
            return 1

    def _calculate_quality_score(self, roe: float, gross_margin: float) -> float:
        """计算质量因子得分"""
        if roe > 20 and gross_margin > 40:
            return 4
        elif roe > 15 and gross_margin > 30:
            return 3
        elif roe > 10 and gross_margin > 20:
            return 2
        else:
            return 1

    def _calculate_liquidity_score(self, volume: float, turnover: float) -> float:
        """计算流动性因子得分"""
        if volume > 1000000 and turnover > 5:
            return 4
        elif volume > 500000 and turnover > 3:
            return 3
        elif volume > 100000 and turnover > 1:
            return 2
        else:
            return 1

    def _generate_investment_advice(self, overall_score: float) -> str:
        """根据综合得分生成投资建议"""
        if overall_score >= 12:
            return "强烈买入：综合得分较高，该股票具有较高的投资价值。建议在当前价位积极买入，仓位可控制在30%-50%。"
        elif overall_score >= 8:
            return "买入：综合得分良好，该股票具有一定的投资价值。建议在当前价位适量买入，仓位可控制在10%-30%。"
        elif overall_score >= 4:
            return "观望：综合得分一般，建议先观望，等待更多信息或股价调整后再做决策。"
        else:
            return "卖出：综合得分较低，该股票投资价值较低。若已持有，建议尽快卖出；未持有则不建议买入。"
