from backend.word_utils import parse_docx_structure, edit_text
from backend.index_finder import find_indices
from backend.llm_client import get_modification_rule
import os

def agent_nl_modify(docx_path: str, user_instruction: str, openai_api_key: str) -> str:
    structure = parse_docx_structure(docx_path)
    paragraphs = structure['paragraphs']
    rule, new_text = get_modification_rule(paragraphs, user_instruction, openai_api_key)
    indices = find_indices(paragraphs, rule)
    if not indices:
        raise ValueError("未找到需要修改的段落")
    # 为保证幂等性，生成新文件
    edited_path = docx_path.replace('.docx', '_agent_edited.docx')
    # 复制原文件
    import shutil
    shutil.copyfile(docx_path, edited_path)
    for idx in indices:
        edit_text(edited_path, 'index', str(idx), 'replace', new_text)
    return edited_path