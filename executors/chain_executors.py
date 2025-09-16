from langchain.agents import create_openai_tools_agent, AgentExecutor

from llm.llm_init import get_chat_openai
from llm.prompt_init import get_prompt_chain
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
    prompt = get_prompt_chain(stock_schema)
    tools = [get_stock_info_csv, get_stock_history, tech_tool, bocha_websearch_tool]
    # tools = [get_stock_info_csv, get_stock_history, tech_tool]
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)
    return executor
