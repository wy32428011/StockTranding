from langchain.agents import create_openai_tools_agent, AgentExecutor
from sqlalchemy.orm import Session

from db.database import get_db
from llm.llm_init import get_chat_openai
from llm.prompt_init import get_prompt_chain, get_prompt
from models.stock_analysis_makdown import StockAnalysisMarkdown, StockAnalysisMarkdownModel
from models.stock_data_report import StockDataReport
from models.stock_report import StockReport
from tools.ak_tools import get_stock_info_csv, get_stock_history, tech_tool
from tools.web_search import bocha_websearch_tool


def get_chain_executor():
    """
    获取链执行器
    :return:
    """
    llm = get_chat_openai()
    # llm = llm.with_structured_output(StockReport)
    stock_schema = str(StockReport.model_json_schema()).replace('{', '{{').replace('}', '}}')
    # prompt = get_prompt_chain(stock_schema)
    prompt = get_prompt()
    tools = [get_stock_info_csv, get_stock_history, tech_tool, bocha_websearch_tool]
    # tools = [get_stock_info_csv, get_stock_history, tech_tool]
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    return executor


async def get_chain_executor_stock_analysis(symbol: str, content: str):
    """
    获取股票分析链执行器
    :param content: 股票数据
    :param symbol: 股票代码
    :return:
    """
    llm = get_chat_openai()
    llm = llm.with_structured_output(StockAnalysisMarkdownModel,method="json_schema")
    # stock_analysis_schema = str(StockAnalysisMarkdown).replace('{', '{{').replace('}', '}}')
    # prompt = get_prompt_chain(stock_analysis_schema)
    db: Session = next(get_db())
    # datas = []
    # data = db.query(StockDataReport).filter(StockDataReport.symbol == symbol).order_by(StockDataReport.analysis_date.desc()).first()
    result = await llm.ainvoke("格式化给出数据,不要省略任何内容，按照类目将对应的内容以markdown形式写入对应字段：" + content)
    print(f"================================>股票分析: {result}")
    # 保存分析结果
    analysis = StockAnalysisMarkdown(
        symbol=symbol,
        stock_name=result.stock_name,
        analysis_date=result.analysis_date,
        fundamental_analysis=result["fundamental_analysis"],
        trading_data_dynamic_analysis=result["trading_data_dynamic_analysis"],
        technical_indicator_analysis=result["technical_indicator_analysis"],
        comprehensive_judgment_and_investment_strategy=result["comprehensive_judgment_and_investment_strategy"],
        conclusion=result["conclusion"]
    )
    db.add(analysis)
    db.commit()
    # return executor
