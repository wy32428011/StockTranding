import json


def get_chat_openai():
    """
    获取OpenAI模型
    :return: OpenAI模型
    """
    from langchain_openai import ChatOpenAI
    from setting.config_setting import LLM_CONFIG
    # llm_config = json.dumps(LLM_CONFIG)
    llm = ChatOpenAI(
        base_url=LLM_CONFIG["base_url"],
        api_key=LLM_CONFIG["api_key"],
        model=LLM_CONFIG["model"],
    )
    return llm


def get_chat_ollama():
    """
    获取Ollama模型
    :return: Ollama模型
    """
    from langchain_ollama import ChatOllama
    from setting.config_setting import OLLAMA_CHAT_CONFIG
    llm = ChatOllama(
        base_url=OLLAMA_CHAT_CONFIG["base_url"],
        model=OLLAMA_CHAT_CONFIG["model"],
    )
    return llm
