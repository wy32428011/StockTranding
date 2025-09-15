# 模型配置
LLM_CONFIG = {
    "base_url": "http://192.168.60.146:9090/v1",
    "api_key": "qwen",
    "model": "qwen"
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
    "host": "192.168.49.222",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "investment_ratings"
}
