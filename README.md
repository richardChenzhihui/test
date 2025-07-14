# 香港律师AI助手

## 功能简介
- 本地法律文档导入与管理
- 基于OpenAI API的智能法律问答
- 本地知识库检索与引用
- 数据本地化，支持备份

## 安装与运行
1. 安装依赖：`pip install -r requirements.txt`
2. 运行：`python main.py`
3. 首次使用请在界面设置API Key
4. 导入法律文档后即可提问

## 打包为exe
1. 安装PyInstaller：`pip install pyinstaller`
2. 打包：`pyinstaller --onefile --add-data "docs;docs" --add-data "data;data" main.py`
3. 在`dist/`目录下获得`main.exe`
