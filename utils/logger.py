from loguru import logger
import os
from config import load_config

def setup_logger():
    config = load_config()
    log_path = config.get("log_path", "data/app.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger.add(log_path, rotation="1 MB", retention="10 days", encoding="utf-8")
    logger.info("Logger initialized.")