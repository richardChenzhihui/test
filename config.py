import os
import json

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".word_agent_config.json")

DEFAULT_CONFIG = {
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    "embedding_model": "text-embedding-ada-002",
    "chat_model": "gpt-3.5-turbo",
    "db_path": "data/chroma_db",
    "log_path": "data/app.log",
    "workspace": "data/workspace",
    "templates_path": "data/templates",
    "max_document_size": 10 * 1024 * 1024,  # 10MB
    "supported_formats": ["docx"],
    "ai_temperature": 0.3,
    "max_tokens": 2000,
    "cache_enabled": True,
    "cache_size": 100,
    "auto_save": True,
    "backup_enabled": True,
    "backup_interval": 300,  # 5 minutes
    "server_host": "0.0.0.0",
    "server_port": 8000,
    "debug": False
}

def load_config():
    """加载配置"""
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 合并默认配置，确保新配置项存在
    merged_config = DEFAULT_CONFIG.copy()
    merged_config.update(config)
    
    return merged_config

def save_config(config):
    """保存配置"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_config_value(key, default=None):
    """获取配置值"""
    config = load_config()
    return config.get(key, default)

def set_config_value(key, value):
    """设置配置值"""
    config = load_config()
    config[key] = value
    save_config(config)

def reset_config():
    """重置配置为默认值"""
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG