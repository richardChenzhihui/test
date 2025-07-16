# 智能 Word Agent 使用指导

## 1. 环境准备
- **操作系统**：Linux/macOS/Windows
- **Python 版本**：建议 3.8 及以上
- **依赖**：见 requirements.txt

## 2. 依赖安装

在项目根目录下执行：

```bash
pip install -r requirements.txt
```

## 3. 目录结构说明

```
/word-editor-agent/
├── backend/
│   ├── main.py             # FastAPI 服务入口
│   ├── agent.py            # 智能 agent 入口
│   ├── word_utils.py       # Word 文档操作
│   ├── index_finder.py     # index 查找工具
│   ├── llm_client.py       # LLM 调用封装
│   ├── schemas.py          # Pydantic 数据结构
│   └── tests/
│       ├── test_api.py     # API 测试
│       └── test_agent.py   # agent 测试（含 LLM mock/实测）
├── requirements.txt
└── test.docx               # 测试用 Word 文档
```

## 4. 启动服务

进入 backend 目录，启动 FastAPI 服务：

```bash
uvicorn backend.main:app --reload
```

服务默认监听 `http://127.0.0.1:8000`，可通过 Swagger UI 访问接口文档：  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## 5. API 使用示例

### 5.1 编辑指定 index 的段落

```bash
curl -F "file=@test.docx" \
     -F "locate_type=index" \
     -F "locate_value=0" \
     -F "op_type=replace" \
     -F "content=新内容" \
     http://127.0.0.1:8000/edit_text
```

### 5.2 智能 agent 自然语言批量修改（需 LLM 支持）

- 通过 Python 代码调用 `agent_nl_modify`，或扩展 main.py 增加 `/agent_nl_modify` API。
- 示例代码（需 OpenAI API Key）：

```python
from backend.agent import agent_nl_modify

edited_path = agent_nl_modify(
    "test.docx",
    "把所有包含‘待办’的段落改成‘已完成’。",
    openai_api_key="sk-xxxxxx"
)
print("修改后文档路径：", edited_path)
```

## 6. 自动化测试

### 6.1 本地 mock LLM 测试

```bash
pytest backend/tests/test_agent.py
```
无需真实 LLM Key，测试会自动 mock LLM 行为。

### 6.2 真实 LLM 测试

1. 准备 `test.docx`，包含“待办”段落。
2. 设置环境变量（推荐 export，避免 key 泄露）：

   ```bash
   export OPENAI_API_KEY=sk-xxxxxx
   ```

3. 运行测试：

   ```bash
   pytest backend/tests/test_agent.py
   ```

   若未设置 `OPENAI_API_KEY`，真实 LLM 测试会自动跳过。

## 7. 常见问题

- **LLM 返回格式不符**：已内置健壮的 JSON 解析，若仍失败请优化 prompt 或升级 LLM。
- **index 查找不准**：可扩展 index_finder 支持 embedding 相似度、复合筛选等。
- **文档内容未变**：请确认测试文档内容、指令与 LLM 返回规则一致。

## 8. 扩展建议

- 支持表格、图片等结构的智能定位与修改
- 前端富文本编辑器集成
- 多轮对话式 agent
- CI/CD 集成自动化测试

---

如需进一步定制、扩展或遇到任何问题，欢迎随时联系开发团队！
