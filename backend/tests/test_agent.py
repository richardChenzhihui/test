import os
import shutil
import tempfile
import pytest
from backend.agent import agent_nl_modify
from backend.word_utils import parse_docx_structure

class DummyLLM:
    """Mock LLM，始终返回关键词查找规则和新内容。"""
    @staticmethod
    def get_modification_rule(paragraphs, user_instruction, openai_api_key):
        return {"type": "keyword", "value": "待办"}, "已完成"

@pytest.fixture(autouse=True)
def patch_llm(monkeypatch):
    from backend import llm_client
    monkeypatch.setattr(llm_client, "get_modification_rule", DummyLLM.get_modification_rule)

@pytest.fixture
def temp_docx():
    # 复制一份测试文档到临时目录
    src = os.path.join(os.path.dirname(__file__), '../test.docx')
    tmpdir = tempfile.mkdtemp()
    dst = os.path.join(tmpdir, 'test.docx')
    shutil.copyfile(src, dst)
    yield dst
    shutil.rmtree(tmpdir)

def test_agent_nl_modify(temp_docx):
    # 指令：把所有包含“待办”的段落改成“已完成”
    edited_path = agent_nl_modify(temp_docx, "把所有包含‘待办’的段落改成‘已完成’。", openai_api_key="dummy")
    structure = parse_docx_structure(edited_path)
    for para in structure['paragraphs']:
        if '待办' in para['text']:
            # 应该都被替换成“已完成”
            assert para['text'] == '已完成'