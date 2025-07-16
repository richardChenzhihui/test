import re
from typing import List, Dict

def find_indices(paragraphs: List[Dict], rule: Dict) -> List[int]:
    """
    paragraphs: List[dict]，每个dict包含 index 和 text
    rule: dict，描述查找规则，如
        {'type': 'keyword', 'value': '待办'}
        {'type': 'regex', 'value': 'TODO.*'}
    返回：符合条件的 index 列表
    """
    indices = []
    if rule['type'] == 'keyword':
        for para in paragraphs:
            if rule['value'] in para['text']:
                indices.append(para['index'])
    elif rule['type'] == 'regex':
        pattern = re.compile(rule['value'])
        for para in paragraphs:
            if pattern.search(para['text']):
                indices.append(para['index'])
    else:
        raise ValueError(f"不支持的查找类型: {rule['type']}")
    return indices