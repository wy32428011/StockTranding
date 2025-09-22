import json


def get_chat_openai():
    """
    获取OpenAI模型
    :return: OpenAI模型
    """
    from langchain_openai import ChatOpenAI
    from setting.config_setting import LLM_CONFIG
    # llm = ChatOpenAI(
    #     base_url=LLM_CONFIG["base_url"],
    #     api_key=LLM_CONFIG["api_key"],
    #     model=LLM_CONFIG["model"],
    # )
    base_url = LLM_CONFIG.get("base_url")
    if not base_url:
        raise ValueError("OpenAI base_url is not configured")
    api_key = LLM_CONFIG.get("api_key")
    if not api_key:
        raise ValueError("OpenAI api_key is not configured")
    model = LLM_CONFIG.get("model")
    if not model:
        raise ValueError("OpenAI model is not configured")
    llm = ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
        model=model,
        max_tokens=2560000
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
