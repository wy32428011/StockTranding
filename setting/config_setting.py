# 模型配置
LLM_CONFIG = {
    "base_url": "http://172.24.205.153:20000/v1",
    "api_key": "qwen",
    "model": "qwen",
    # "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    # "api_key": "sk-63affe170adb4389b2e50438e923d116",
    # "model": "qwen-plus-2025-07-28"
}
# Ollama模型配置
OLLAMA_CHAT_CONFIG = {
    "base_url": "http://localhost:11434/v1",
    "api_key": "ollama",
    "model": "llama2"
}
# 数据库配置
DB_CONFIG = {
    "type": "mysql",
    "host": "192.168.50.19",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "investment_ratings"
}
ALLTICK_CONFIG = {
    "ALLTICK_API_KEY": "09ab7e110950969ece587b50aa87ede9-c-app"
}
SYSTEM_CONFIG = {
    "bocha_websearch" : {
        "ENABLED": False,
        "BOCHA_API_URL": "https://api.bochaai.com/v1/web-search",
        "BOCHA_API_KEY": "sk-bdce09f8b03a4adaa2a806f75099e42e"
    }
}