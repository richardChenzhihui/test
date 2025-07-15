#!/usr/bin/env python3
"""
Word Agent 项目设置脚本
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """检查 Python 版本"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ 是必需的")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python 版本: {sys.version}")
    return True

def install_dependencies():
    """安装依赖包"""
    print("\n📦 安装依赖包...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ 依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def create_directories():
    """创建必要的目录"""
    print("\n📁 创建目录结构...")
    directories = [
        "data/workspace",
        "data/templates", 
        "examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ 创建目录: {directory}")

def setup_config():
    """设置配置"""
    print("\n⚙️  配置设置...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  未找到 OpenAI API Key 环境变量")
        api_key = input("请输入您的 OpenAI API Key (或按 Enter 跳过): ").strip()
    
    if api_key:
        config_path = Path.home() / ".word_agent_config.json"
        config = {
            "openai_api_key": api_key,
            "chat_model": "gpt-3.5-turbo",
            "workspace": "data/workspace",
            "server_port": 8000
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ 配置文件已创建")
    else:
        print("⚠️  跳过 API Key 配置，稍后请手动设置")

def create_example_files():
    """创建示例文件"""
    print("\n📄 创建示例文件...")
    
    # 创建一个简单的测试脚本
    test_script = """#!/usr/bin/env python3
import requests
import json

def test_word_agent():
    base_url = "http://localhost:8000"
    
    # 健康检查
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"服务状态: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请先启动服务器")
        return
    
    # 创建测试文档
    response = requests.post(f"{base_url}/api/word/create", json={
        "title": "测试文档",
        "initial_content": "这是一个测试文档"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 文档创建成功: {result.get('document_path')}")
    else:
        print(f"❌ 文档创建失败: {response.text}")

if __name__ == "__main__":
    test_word_agent()
"""
    
    with open("examples/test_connection.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ 示例文件已创建")

def main():
    """主函数"""
    print("🚀 Word Agent 项目设置")
    print("=" * 40)
    
    # 检查 Python 版本
    if not check_python_version():
        return
    
    # 创建目录
    create_directories()
    
    # 安装依赖
    if not install_dependencies():
        print("❌ 设置失败，请检查依赖包安装")
        return
    
    # 设置配置
    setup_config()
    
    # 创建示例文件
    create_example_files()
    
    print("\n🎉 设置完成！")
    print("\n下一步:")
    print("1. 启动服务器: python word_agent_server.py")
    print("2. 访问 API 文档: http://localhost:8000/docs")
    print("3. 运行示例: python examples/word_agent_examples.py")
    print("4. 测试连接: python examples/test_connection.py")

if __name__ == "__main__":
    main()