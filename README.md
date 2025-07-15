# Word Agent - AI 驱动的 Word 文档智能编辑器

基于 Python 的 Word 文档智能编辑 Agent，通过自然语言指令和 AI 大模型接口实现 Word 文档的自动化编辑功能。

## 功能特性

### 核心功能
- ✅ 自然语言指令解析
- ✅ 文档内容编辑（添加、删除、修改）
- ✅ 表格操作（创建、编辑、删除）
- ✅ 样式设置（字体、颜色、大小）
- ✅ 格式化操作（段落、标题、列表）
- ✅ 文档创建和管理
- ✅ RESTful API 接口

### 技术特点
- 🚀 基于 FastAPI 的高性能 API 服务
- 🤖 OpenAI GPT 模型支持
- 📝 Python-docx 文档处理
- 🔄 智能指令解析和操作执行
- 💾 文档缓存和版本管理
- 📊 完整的日志记录

## 系统架构

```
┌─────────────────────────────────────┐
│           API Layer                  │  FastAPI RESTful API
├─────────────────────────────────────┤
│        Service Layer                │  业务逻辑处理
├─────────────────────────────────────┤
│      Word Agent Engine              │  核心 Agent 引擎
├─────────────────────────────────────┤
│     Document Processor              │  文档处理器
├─────────────────────────────────────┤
│        AI Interface                 │  大模型接口
└─────────────────────────────────────┘
```

## 项目结构

```
word_agent/
├── api/                      # API 层
│   ├── models.py            # 数据模型
│   └── word_api.py          # FastAPI 应用
├── word_agent/              # 核心引擎
│   ├── agent_engine.py      # 主引擎
│   └── command_parser.py    # 指令解析器
├── document/                # 文档处理
│   └── word_processor.py    # Word 文档处理器
├── ai/                      # AI 接口
│   ├── openai_api.py        # OpenAI API 接口
│   └── prompt_templates.py  # 提示词模板
├── utils/                   # 工具模块
│   ├── logger.py           # 日志工具
│   └── doc_parser.py       # 文档解析
├── examples/                # 使用示例
│   └── word_agent_examples.py
├── config.py               # 配置管理
├── requirements.txt        # 依赖包
├── word_agent_server.py    # 服务器启动脚本
└── README.md              # 项目说明
```

## 快速开始

### 1. 环境要求
- Python 3.8+
- pip 包管理器
- OpenAI API Key

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置设置

设置 OpenAI API Key：

```bash
export OPENAI_API_KEY="your-api-key-here"
```

或者在配置文件中设置：

```python
# config.py
DEFAULT_CONFIG = {
    "openai_api_key": "your-api-key-here",
    # ... 其他配置
}
```

### 4. 启动服务

```bash
python word_agent_server.py
```

服务启动后，访问 http://localhost:8000/docs 查看 API 文档。

## API 使用指南

### 核心接口

#### 1. 创建文档
```http
POST /api/word/create
Content-Type: application/json

{
  "title": "我的文档",
  "initial_content": "这是初始内容"
}
```

#### 2. 处理指令
```http
POST /api/word/process
Content-Type: application/json

{
  "instruction": "添加一个标题：产品介绍",
  "document_path": "path/to/document.docx"
}
```

#### 3. 获取预览
```http
GET /api/word/preview?document_path=path/to/document.docx
```

#### 4. 文件管理
```http
GET /api/word/files                    # 列出文件
GET /api/word/download/{filename}      # 下载文件
POST /api/word/upload                  # 上传文件
DELETE /api/word/files/{filename}      # 删除文件
```

### 支持的指令示例

```python
# 文本操作
"添加内容：这是一段新的文本"
"删除文本：要删除的内容"
"修改文本：将'旧文本'改为'新文本'"

# 标题操作
"添加一级标题：章节标题"
"添加二级标题：子章节标题"

# 表格操作
"创建一个3行4列的表格"
"添加表格，表头为：姓名、年龄、职业"

# 样式设置
"设置文本为粗体，字号14"
"将标题颜色设为红色"

# 列表操作
"添加无序列表：项目1、项目2、项目3"
"创建有序列表：步骤1、步骤2、步骤3"
```

## 使用示例

### Python 客户端示例

```python
import requests

# 创建文档
response = requests.post('http://localhost:8000/api/word/create', json={
    "title": "测试文档",
    "initial_content": "这是一个测试文档"
})
result = response.json()
document_path = result['document_path']

# 添加内容
response = requests.post('http://localhost:8000/api/word/process', json={
    "instruction": "添加一个二级标题：产品特性",
    "document_path": document_path
})

# 获取预览
response = requests.get('http://localhost:8000/api/word/preview', params={
    "document_path": document_path
})
preview = response.json()['preview_text']
print(preview)
```

### 运行示例代码

```bash
cd examples
python word_agent_examples.py
```

## 高级功能

### 1. 自定义操作

可以通过直接传递操作列表来精确控制文档编辑：

```python
operations = [
    {
        "operation_type": "add_heading",
        "content": "重要通知",
        "metadata": {"level": 1},
        "style": {
            "font_size": 16,
            "bold": True,
            "color": "#FF0000"
        }
    },
    {
        "operation_type": "add_table",
        "table_data": {
            "rows": 2,
            "cols": 3,
            "headers": ["列1", "列2", "列3"],
            "data": [["数据1", "数据2", "数据3"]]
        }
    }
]
```

### 2. 样式定制

支持丰富的样式设置：

```python
style = {
    "font_name": "Arial",
    "font_size": 12,
    "bold": True,
    "italic": False,
    "underline": True,
    "color": "#0000FF"
}
```

### 3. 批量处理

可以批量处理多个文档或执行多个操作：

```python
# 批量执行多个指令
instructions = [
    "添加标题：第一章",
    "添加内容：这是第一章的内容",
    "添加标题：第二章",
    "添加内容：这是第二章的内容"
]
```

## 配置选项

在 `config.py` 中可以配置以下选项：

```python
{
    "openai_api_key": "",           # OpenAI API Key
    "chat_model": "gpt-3.5-turbo",  # 使用的模型
    "workspace": "data/workspace",   # 工作目录
    "max_document_size": 10485760,   # 最大文档大小
    "ai_temperature": 0.3,           # AI 温度参数
    "max_tokens": 2000,              # 最大 token 数
    "cache_enabled": True,           # 是否启用缓存
    "auto_save": True,               # 是否自动保存
    "server_port": 8000              # 服务器端口
}
```

## 部署说明

### 开发环境
```bash
python word_agent_server.py
```

### 生产环境
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api.word_api:app
```

### Docker 部署
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "word_agent_server.py"]
```

## 故障排除

### 常见问题

1. **OpenAI API 错误**
   - 确保 API Key 正确设置
   - 检查网络连接
   - 验证 API 配额

2. **文档处理错误**
   - 确保文档格式正确 (.docx)
   - 检查文件权限
   - 验证文档是否损坏

3. **服务启动失败**
   - 检查端口是否被占用
   - 确保依赖包正确安装
   - 查看日志文件

### 日志查看

```bash
tail -f data/app.log
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的文档编辑功能
- 提供 RESTful API 接口
- 集成 OpenAI GPT 模型

---

**注意**: 本项目目前处于 MVP 阶段，功能持续完善中。如有问题或建议，请提交 Issue。
