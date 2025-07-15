"""
AI 提示词模板
"""

INSTRUCTION_PARSE_PROMPT = """你是一个专业的 Word 文档编辑助手。请将用户的自然语言指令转换为具体的文档操作。

用户指令: {instruction}
当前文档内容: {document_content}

请根据指令生成相应的操作，返回 JSON 格式的操作列表。每个操作应包含以下字段：
- operation_type: 操作类型 (add_text, delete_text, modify_text, add_table, modify_table, delete_table, set_style, set_font, add_heading, add_list, insert_image)
- content: 操作内容
- position: 插入位置 (可选，默认为 "end")
- style: 样式设置 (可选)
- table_data: 表格数据 (可选)
- metadata: 其他元数据 (可选)

支持的操作类型说明：
1. add_text: 添加文本内容
2. delete_text: 删除指定文本
3. modify_text: 修改文本（需要在metadata中指定old_text）
4. add_table: 添加表格
5. add_heading: 添加标题（需要在metadata中指定level）
6. add_list: 添加列表（需要在metadata中指定items和ordered）
7. set_style: 设置样式
8. set_font: 设置字体

样式设置字段：
- font_name: 字体名称
- font_size: 字体大小
- bold: 是否粗体
- italic: 是否斜体
- underline: 是否下划线
- color: 字体颜色 (十六进制格式，如 #FF0000)

请严格按照 JSON 格式返回，不要添加任何额外的文本说明：
```json
[
  {{
    "operation_type": "操作类型",
    "content": "内容",
    "position": "位置",
    "style": {{
      "font_name": "字体名称",
      "font_size": 字体大小,
      "bold": true/false,
      "italic": true/false,
      "underline": true/false,
      "color": "#颜色代码"
    }},
    "table_data": {{
      "rows": 行数,
      "cols": 列数,
      "headers": ["表头1", "表头2"],
      "data": [["数据1", "数据2"], ["数据3", "数据4"]]
    }},
    "metadata": {{
      "key": "value"
    }}
  }}
]
```
"""

STYLE_RECOMMENDATION_PROMPT = """你是一个专业的文档格式设计师。请根据以下文档内容和用户需求，推荐合适的样式设置。

文档内容: {document_content}
用户需求: {user_requirement}

请推荐以下方面的样式设置：
1. 标题样式（字体、大小、颜色、格式）
2. 正文样式（字体、大小、行间距）
3. 表格样式（边框、背景色、字体）
4. 列表样式（符号、缩进、间距）
5. 强调文本样式（粗体、斜体、颜色）

请返回 JSON 格式的推荐样式：
```json
{{
  "title_style": {{
    "font_name": "字体名称",
    "font_size": 字体大小,
    "bold": true,
    "color": "#颜色代码"
  }},
  "body_style": {{
    "font_name": "字体名称",
    "font_size": 字体大小,
    "color": "#颜色代码"
  }},
  "table_style": {{
    "header_style": {{
      "bold": true,
      "color": "#颜色代码"
    }},
    "body_style": {{
      "font_size": 字体大小,
      "color": "#颜色代码"
    }}
  }},
  "emphasis_style": {{
    "bold": true,
    "italic": false,
    "color": "#颜色代码"
  }}
}}
```
"""

CONTENT_GENERATION_PROMPT = """你是一个专业的内容创作助手。请根据用户的需求生成合适的文档内容。

用户需求: {user_requirement}
文档类型: {document_type}
目标受众: {target_audience}

请生成结构化的文档内容，包括：
1. 标题层级结构
2. 段落内容
3. 表格内容（如需要）
4. 列表内容（如需要）

请返回 JSON 格式的内容结构：
```json
{{
  "title": "文档标题",
  "sections": [
    {{
      "heading": "章节标题",
      "level": 1,
      "content": "章节内容",
      "subsections": [
        {{
          "heading": "子章节标题",
          "level": 2,
          "content": "子章节内容"
        }}
      ]
    }}
  ],
  "tables": [
    {{
      "title": "表格标题",
      "position": "章节标题",
      "headers": ["列1", "列2"],
      "data": [["数据1", "数据2"]]
    }}
  ],
  "lists": [
    {{
      "type": "bullet",
      "position": "章节标题",
      "items": ["项目1", "项目2"]
    }}
  ]
}}
```
"""

ERROR_ANALYSIS_PROMPT = """你是一个文档编辑错误分析专家。请分析以下操作失败的原因，并提供解决方案。

操作描述: {operation_description}
错误信息: {error_message}
文档状态: {document_status}

请分析：
1. 失败的可能原因
2. 推荐的解决方案
3. 预防措施

请返回 JSON 格式的分析结果：
```json
{{
  "error_cause": "错误原因分析",
  "solution": "解决方案",
  "prevention": "预防措施",
  "alternative_operations": [
    {{
      "operation_type": "替代操作类型",
      "description": "操作描述"
    }}
  ]
}}
```
"""

DOCUMENT_SUMMARY_PROMPT = """你是一个文档分析专家。请分析以下文档内容并生成摘要。

文档内容: {document_content}

请生成：
1. 文档结构摘要
2. 主要内容要点
3. 文档统计信息
4. 改进建议

请返回 JSON 格式的摘要：
```json
{{
  "structure_summary": {{
    "total_paragraphs": 段落数量,
    "total_headings": 标题数量,
    "total_tables": 表格数量,
    "total_lists": 列表数量
  }},
  "content_summary": "内容摘要",
  "key_points": ["要点1", "要点2"],
  "statistics": {{
    "word_count": 字数,
    "character_count": 字符数,
    "estimated_reading_time": "阅读时间"
  }},
  "improvement_suggestions": ["建议1", "建议2"]
}}
```
"""