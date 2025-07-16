import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_edit_text():
    test_file = os.path.join(os.path.dirname(__file__), '../test.docx')
    with open(test_file, 'rb') as f:
        response = client.post(
            "/edit_text",
            files={"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            data={
                "locate_type": "index",
                "locate_value": "0",
                "op_type": "replace",
                "content": "新内容"
            }
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"]
    assert "download_url" in data
    assert "structure" in data

def test_parse():
    test_file = os.path.join(os.path.dirname(__file__), '../test.docx')
    with open(test_file, 'rb') as f:
        response = client.post(
            "/parse",
            files={"file": ("test.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "paragraphs" in data
    assert "tables" in data