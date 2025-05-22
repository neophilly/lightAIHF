# -*- coding: utf-8 -*-

import requests
from typing import Dict, Any, Optional
import logging

class AIAnalyzer:
    def __init__(self, model: str = "deepseek-coder-v2:16b", host: str = "http://localhost:11434"):
        """Initialize the AI Analyzer.
        
        Args:
            model (str): The Ollama model to use (e.g., 'mistral', 'llama2', 'codellama')
            host (str): The Ollama API host address
        """
        self.model = model
        self.host = host
        self.api_endpoint = f"{host}/api/generate"
        
    def analyze_stock(self, stock_data: Dict[str, Any]) -> Optional[str]:
        """Analyze stock data using the AI model.
        
        Args:
            stock_data: Dictionary containing stock information and metrics
            
        Returns:
            str: AI-generated analysis and recommendations
        """
        try:
            # Prepare the prompt
            prompt = self._create_analysis_prompt(stock_data)
            
            # Call Ollama API with proper encoding
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Accept-Charset": "utf-8"
                }
            )
            
            if response.status_code == 200:
                # Ensure proper UTF-8 decoding
                result = response.json()["response"]
                return result.encode('utf-8').decode('utf-8')
            else:
                logging.error(f"获取AI分析失败: {response.status_code}")
                return None
                
        except Exception as e:
            logging.error(f"AI分析过程中出现错误: {str(e)}")
            return None
            
    def _create_analysis_prompt(self, stock_data: Dict[str, Any]) -> str:
        """Create a detailed prompt for the AI model."""
        return f"""请用中文分析以下股票数据并提供投资建议：

股票信息：
- 名称: {stock_data.get('name', '未知')}
- 代码: {stock_data.get('ts_code', '未知')}
- 当前价格: {stock_data.get('price', '未知')}
- 市盈率(PE): {stock_data.get('pe_ttm', '未知')}
- 市净率(PB): {stock_data.get('pb', '未知')}
- 净资产收益率(ROE): {stock_data.get('roe', '未知')}%
- 资产负债率: {stock_data.get('debt_ratio', '未知')}%
- 股息率: {stock_data.get('dividend_yield', '未知')}%

请提供以下分析：
1. 市场地位分析
   - 行业地位
   - 竞争优势
   - 市场份额

2. 财务健康状况
   - 盈利能力
   - 资产质量
   - 现金流状况

3. 风险分析
   - 市场风险
   - 财务风险
   - 经营风险

4. 投资建议
   - 投资评级
   - 目标价位
   - 建仓策略

5. 重点监控指标
   - 关键财务指标
   - 技术指标
   - 风险指标

请以清晰的结构化格式输出，使用标题、要点和分段来组织内容。对每个分析点给出具体的数据支持和理由。""" 