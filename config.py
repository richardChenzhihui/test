import os
import json

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".lawyer_ai_config.json")

DEFAULT_CONFIG = {
    "openai_api_key": "",
    "embedding_model": "text-embedding-ada-002",
    "chat_model": "gpt-3.5-turbo",
    "db_path": "data/chroma_db",
    "log_path": "data/app.log"
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)