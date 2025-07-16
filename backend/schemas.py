from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class EditTextRequest(BaseModel):
    file_path: str = Field(..., description="Word 文件路径")
    locate_type: Literal['index', 'regex', 'nl'] = Field(..., description="定位方式：index/正则/自然语言")
    locate_value: str = Field(..., description="定位值")
    op_type: Literal['insert', 'replace', 'delete'] = Field(..., description="操作类型")
    content: Optional[str] = Field(None, description="插入或替换的内容")

class EditTextResponse(BaseModel):
    success: bool
    download_url: Optional[str] = None
    message: Optional[str] = None
    structure: Optional[dict] = None

class ParseRequest(BaseModel):
    file_path: str

class Paragraph(BaseModel):
    index: int
    text: str

class TableCell(BaseModel):
    row: int
    col: int
    text: str

class Table(BaseModel):
    index: int
    rows: int
    cols: int
    content: List[List[str]]

class ParseResponse(BaseModel):
    paragraphs: List[Paragraph]
    tables: List[Table]