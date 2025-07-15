#!/usr/bin/env python3
"""
Word Agent 服务器启动脚本
"""

import uvicorn
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from api.word_api import app
from config import load_config
from utils.logger import setup_logger

def main():
    """主函数"""
    logger = setup_logger()
    config = load_config()
    
    # 检查 OpenAI API Key
    if not config.get('openai_api_key'):
        logger.error("请配置 OpenAI API Key")
        logger.info("可以通过以下方式配置:")
        logger.info("1. 在 config.py 中设置 DEFAULT_CONFIG['openai_api_key']")
        logger.info("2. 或者设置环境变量 OPENAI_API_KEY")
        return
    
    # 创建工作目录
    workspace = config.get('workspace', 'data/workspace')
    os.makedirs(workspace, exist_ok=True)
    
    # 启动服务器
    logger.info("启动 Word Agent 服务器...")
    logger.info(f"工作目录: {workspace}")
    logger.info("API 文档地址: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()