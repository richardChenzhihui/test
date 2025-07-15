from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class OperationType(str, Enum):
    """操作类型枚举"""
    ADD_TEXT = "add_text"
    DELETE_TEXT = "delete_text"
    MODIFY_TEXT = "modify_text"
    ADD_TABLE = "add_table"
    MODIFY_TABLE = "modify_table"
    DELETE_TABLE = "delete_table"
    SET_STYLE = "set_style"
    SET_FONT = "set_font"
    ADD_HEADING = "add_heading"
    ADD_LIST = "add_list"
    INSERT_IMAGE = "insert_image"

class DocumentFormat(str, Enum):
    """文档格式枚举"""
    DOCX = "docx"
    PDF = "pdf"
    HTML = "html"

class TextStyle(BaseModel):
    """文本样式模型"""
    font_name: Optional[str] = Field(default=None, description="字体名称")
    font_size: Optional[int] = Field(default=None, description="字体大小")
    bold: Optional[bool] = Field(default=None, description="是否粗体")
    italic: Optional[bool] = Field(default=None, description="是否斜体")
    underline: Optional[bool] = Field(default=None, description="是否下划线")
    color: Optional[str] = Field(default=None, description="字体颜色")

class TableData(BaseModel):
    """表格数据模型"""
    rows: int = Field(description="行数")
    cols: int = Field(description="列数")
    headers: Optional[List[str]] = Field(default=None, description="表头")
    data: Optional[List[List[str]]] = Field(default=None, description="表格数据")

class WordOperation(BaseModel):
    """Word操作模型"""
    operation_type: OperationType = Field(description="操作类型")
    content: Optional[str] = Field(default=None, description="操作内容")
    position: Optional[str] = Field(default=None, description="插入位置")
    style: Optional[TextStyle] = Field(default=None, description="样式设置")
    table_data: Optional[TableData] = Field(default=None, description="表格数据")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="其他元数据")

class ProcessRequest(BaseModel):
    """处理请求模型"""
    instruction: str = Field(description="自然语言指令")
    document_path: Optional[str] = Field(default=None, description="文档路径")
    operations: Optional[List[WordOperation]] = Field(default=None, description="具体操作列表")

class ProcessResponse(BaseModel):
    """处理响应模型"""
    success: bool = Field(description="是否成功")
    message: str = Field(description="响应消息")
    document_path: Optional[str] = Field(default=None, description="处理后的文档路径")
    operations_performed: Optional[List[WordOperation]] = Field(default=None, description="执行的操作")
    preview_text: Optional[str] = Field(default=None, description="预览文本")

class CreateDocumentRequest(BaseModel):
    """创建文档请求模型"""
    title: str = Field(description="文档标题")
    template_path: Optional[str] = Field(default=None, description="模板路径")
    initial_content: Optional[str] = Field(default=None, description="初始内容")

class ExportRequest(BaseModel):
    """导出请求模型"""
    document_path: str = Field(description="源文档路径")
    export_format: DocumentFormat = Field(description="导出格式")
    output_path: Optional[str] = Field(default=None, description="输出路径")