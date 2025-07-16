import openai
import json
import re
from typing import List, Dict, Tuple

def get_modification_rule(paragraphs: List[Dict], user_instruction: str, openai_api_key: str) -> Tuple[Dict, str]:
    prompt = f"""文档结构如下：\n" + "\n".join([f"{p['index']}: {p['text']}" for p in paragraphs]) + f"\n用户指令：“{user_instruction}”\n请只返回查找规则（如关键词/正则）和新内容，格式为：\n{{\n  \"rule\": {{\"type\": \"keyword\", \"value\": \"待办\"}},\n  \"new_text\": \"已完成\"\n}}\n不要输出任何解释。"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        api_key=openai_api_key
    )
    content = response['choices'][0]['message']['content']
    # 尝试直接解析
    try:
        result = json.loads(content)
        rule = result['rule']
        new_text = result['new_text']
        return rule, new_text
    except Exception:
        # 尝试提取 JSON 块
        match = re.search(r'\{[\s\S]*\}', content)
        if match:
            try:
                result = json.loads(match.group(0))
                rule = result['rule']
                new_text = result['new_text']
                return rule, new_text
            except Exception:
                pass
        raise RuntimeError(f"LLM返回内容解析失败: {content}")