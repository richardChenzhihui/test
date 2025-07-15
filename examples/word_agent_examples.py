#!/usr/bin/env python3
"""
Word Agent 使用示例
"""

import requests
import json
import os
from typing import Dict, Any

class WordAgentClient:
    """Word Agent 客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def process_instruction(self, instruction: str, document_path: str = None) -> Dict[str, Any]:
        """处理指令"""
        url = f"{self.base_url}/api/word/process"
        data = {
            "instruction": instruction,
            "document_path": document_path
        }
        response = self.session.post(url, json=data)
        return response.json()
    
    def create_document(self, title: str, initial_content: str = None) -> Dict[str, Any]:
        """创建文档"""
        url = f"{self.base_url}/api/word/create"
        data = {
            "title": title,
            "initial_content": initial_content
        }
        response = self.session.post(url, json=data)
        return response.json()
    
    def get_preview(self, document_path: str) -> Dict[str, Any]:
        """获取预览"""
        url = f"{self.base_url}/api/word/preview"
        params = {"document_path": document_path}
        response = self.session.get(url, params=params)
        return response.json()
    
    def list_files(self) -> Dict[str, Any]:
        """列出文件"""
        url = f"{self.base_url}/api/word/files"
        response = self.session.get(url)
        return response.json()
    
    def download_file(self, filename: str, save_path: str) -> bool:
        """下载文件"""
        url = f"{self.base_url}/api/word/download/{filename}"
        response = self.session.get(url)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        return False
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        url = f"{self.base_url}/api/health"
        response = self.session.get(url)
        return response.json()

def example_1_basic_usage():
    """示例1：基础用法"""
    print("=== 示例1：基础用法 ===")
    
    client = WordAgentClient()
    
    # 检查服务状态
    health = client.health_check()
    print(f"服务状态: {health}")
    
    # 创建新文档
    result = client.create_document(
        title="我的第一个文档",
        initial_content="这是文档的开始内容。"
    )
    print(f"创建文档结果: {result}")
    
    if result.get('success'):
        document_path = result['document_path']
        
        # 添加标题
        result = client.process_instruction(
            instruction="添加一个二级标题：产品介绍",
            document_path=document_path
        )
        print(f"添加标题结果: {result}")
        
        # 添加内容
        result = client.process_instruction(
            instruction="添加内容：我们的产品是一个创新的解决方案，能够帮助用户提高工作效率。",
            document_path=document_path
        )
        print(f"添加内容结果: {result}")
        
        # 获取预览
        preview = client.get_preview(document_path)
        print(f"文档预览: {preview.get('preview_text', '')[:200]}...")

def example_2_table_operations():
    """示例2：表格操作"""
    print("\n=== 示例2：表格操作 ===")
    
    client = WordAgentClient()
    
    # 创建包含表格的文档
    result = client.create_document(
        title="产品价格表",
        initial_content="以下是我们的产品价格表："
    )
    
    if result.get('success'):
        document_path = result['document_path']
        
        # 添加表格
        result = client.process_instruction(
            instruction="创建一个3行3列的表格，表头为：产品名称、价格、描述",
            document_path=document_path
        )
        print(f"添加表格结果: {result}")
        
        # 获取预览
        preview = client.get_preview(document_path)
        print(f"表格文档预览: {preview.get('preview_text', '')[:200]}...")

def example_3_style_formatting():
    """示例3：样式格式化"""
    print("\n=== 示例3：样式格式化 ===")
    
    client = WordAgentClient()
    
    # 创建带样式的文档
    result = client.create_document(
        title="样式示例文档",
        initial_content="这是一个展示不同样式的文档。"
    )
    
    if result.get('success'):
        document_path = result['document_path']
        
        # 添加带样式的文本
        result = client.process_instruction(
            instruction="添加一段文本'重要提醒：请仔细阅读以下内容'，设置为粗体，字体大小为14，颜色为红色",
            document_path=document_path
        )
        print(f"添加样式文本结果: {result}")
        
        # 添加列表
        result = client.process_instruction(
            instruction="添加一个无序列表，包含以下项目：第一项、第二项、第三项",
            document_path=document_path
        )
        print(f"添加列表结果: {result}")

def example_4_complex_document():
    """示例4：复杂文档创建"""
    print("\n=== 示例4：复杂文档创建 ===")
    
    client = WordAgentClient()
    
    # 创建复杂文档
    result = client.create_document(
        title="项目报告",
        initial_content="这是一份详细的项目报告。"
    )
    
    if result.get('success'):
        document_path = result['document_path']
        
        # 添加多个章节
        sections = [
            ("项目概述", "本项目旨在开发一个创新的AI应用。"),
            ("技术方案", "我们采用了最新的人工智能技术。"),
            ("实施计划", "项目计划分为三个阶段进行。"),
            ("预期效果", "预计能够显著提高工作效率。")
        ]
        
        for title, content in sections:
            # 添加标题
            result = client.process_instruction(
                instruction=f"添加二级标题：{title}",
                document_path=document_path
            )
            print(f"添加标题 '{title}' 结果: {result.get('success', False)}")
            
            # 添加内容
            result = client.process_instruction(
                instruction=f"添加内容：{content}",
                document_path=document_path
            )
            print(f"添加内容结果: {result.get('success', False)}")
        
        # 获取最终预览
        preview = client.get_preview(document_path)
        print(f"复杂文档预览: {preview.get('preview_text', '')[:300]}...")

def example_5_file_management():
    """示例5：文件管理"""
    print("\n=== 示例5：文件管理 ===")
    
    client = WordAgentClient()
    
    # 列出所有文件
    files = client.list_files()
    print(f"工作区文件数量: {files.get('total', 0)}")
    
    for file_info in files.get('files', []):
        print(f"文件: {file_info['filename']}, 大小: {file_info['size']} bytes")
    
    # 下载文件（如果存在）
    if files.get('files'):
        first_file = files['files'][0]
        filename = first_file['filename']
        save_path = f"downloaded_{filename}"
        
        if client.download_file(filename, save_path):
            print(f"文件 {filename} 下载成功，保存为 {save_path}")
        else:
            print(f"文件 {filename} 下载失败")

def run_all_examples():
    """运行所有示例"""
    print("Word Agent 使用示例演示")
    print("=" * 50)
    
    try:
        example_1_basic_usage()
        example_2_table_operations()
        example_3_style_formatting()
        example_4_complex_document()
        example_5_file_management()
        
        print("\n=" * 50)
        print("所有示例执行完成！")
        
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到 Word Agent 服务器")
        print("请确保服务器正在运行：python word_agent_server.py")
    except Exception as e:
        print(f"执行示例时发生错误: {e}")

if __name__ == "__main__":
    run_all_examples()