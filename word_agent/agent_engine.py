from typing import List, Optional, Dict, Any, Tuple
import os
import uuid
from datetime import datetime

from ai.openai_api import OpenAIAPI
from document.word_processor import WordProcessor
from word_agent.command_parser import CommandParser
from api.models import (
    WordOperation, ProcessRequest, ProcessResponse, 
    CreateDocumentRequest, ExportRequest, DocumentFormat
)
from config import load_config
from utils.logger import setup_logger


class WordAgent:
    """Word Agent 核心引擎"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """初始化 Word Agent
        
        Args:
            config: 配置字典
        """
        self.config = config or load_config()
        self.logger = setup_logger()
        
        # 初始化 AI 接口
        self.openai_api = OpenAIAPI(
            api_key=self.config.get('openai_api_key', ''),
            model=self.config.get('chat_model', 'gpt-3.5-turbo')
        )
        
        # 初始化指令解析器
        self.command_parser = CommandParser(self.openai_api)
        
        # 工作目录
        self.workspace = self.config.get('workspace', 'data/workspace')
        os.makedirs(self.workspace, exist_ok=True)
        
        # 文档缓存
        self.document_cache: Dict[str, WordProcessor] = {}
    
    def process_instruction(self, request: ProcessRequest) -> ProcessResponse:
        """处理指令请求
        
        Args:
            request: 处理请求
            
        Returns:
            处理响应
        """
        try:
            self.logger.info(f"处理指令: {request.instruction}")
            
            # 获取或创建文档处理器
            processor = self._get_or_create_processor(request.document_path)
            
            # 获取当前文档内容
            current_content = processor.get_document_text()
            
            # 解析指令
            if request.operations:
                # 如果直接提供了操作列表
                operations = request.operations
            else:
                # 使用AI解析自然语言指令
                operations = self.command_parser.parse_instruction(
                    request.instruction,
                    current_content
                )
            
            # 验证操作
            valid_operations = self.command_parser.validate_operations(operations)
            
            if not valid_operations:
                return ProcessResponse(
                    success=False,
                    message="无法解析指令或操作无效"
                )
            
            # 执行操作
            results = processor.execute_operations(valid_operations)
            
            # 保存文档
            output_path = self._generate_output_path(request.document_path)
            save_success = processor.save_document(output_path)
            
            if not save_success:
                return ProcessResponse(
                    success=False,
                    message="文档保存失败"
                )
            
            # 获取预览内容
            preview_text = processor.get_document_text()[:500]
            
            # 统计成功执行的操作
            successful_operations = [
                op for op, result in zip(valid_operations, results) if result
            ]
            
            return ProcessResponse(
                success=True,
                message=f"成功执行 {len(successful_operations)} 个操作",
                document_path=output_path,
                operations_performed=successful_operations,
                preview_text=preview_text
            )
            
        except Exception as e:
            self.logger.error(f"处理指令失败: {e}")
            return ProcessResponse(
                success=False,
                message=f"处理失败: {str(e)}"
            )
    
    def create_document(self, request: CreateDocumentRequest) -> ProcessResponse:
        """创建新文档
        
        Args:
            request: 创建文档请求
            
        Returns:
            处理响应
        """
        try:
            self.logger.info(f"创建文档: {request.title}")
            
            # 创建新的文档处理器
            processor = WordProcessor(request.template_path)
            
            # 添加标题
            if request.title:
                processor.add_heading(request.title, level=1)
            
            # 添加初始内容
            if request.initial_content:
                processor.add_text(request.initial_content)
            
            # 生成文档路径
            document_path = self._generate_document_path(request.title)
            
            # 保存文档
            save_success = processor.save_document(document_path)
            
            if not save_success:
                return ProcessResponse(
                    success=False,
                    message="文档创建失败"
                )
            
            # 缓存文档处理器
            self.document_cache[document_path] = processor
            
            return ProcessResponse(
                success=True,
                message="文档创建成功",
                document_path=document_path,
                preview_text=processor.get_document_text()[:500]
            )
            
        except Exception as e:
            self.logger.error(f"创建文档失败: {e}")
            return ProcessResponse(
                success=False,
                message=f"创建失败: {str(e)}"
            )
    
    def export_document(self, request: ExportRequest) -> ProcessResponse:
        """导出文档
        
        Args:
            request: 导出请求
            
        Returns:
            处理响应
        """
        try:
            self.logger.info(f"导出文档: {request.document_path}")
            
            if not os.path.exists(request.document_path):
                return ProcessResponse(
                    success=False,
                    message="源文档不存在"
                )
            
            # 目前只支持 DOCX 格式
            if request.export_format == DocumentFormat.DOCX:
                # 直接复制文件
                output_path = request.output_path or self._generate_export_path(
                    request.document_path, request.export_format
                )
                
                import shutil
                shutil.copy2(request.document_path, output_path)
                
                return ProcessResponse(
                    success=True,
                    message="导出成功",
                    document_path=output_path
                )
            else:
                return ProcessResponse(
                    success=False,
                    message=f"暂不支持导出为 {request.export_format.value} 格式"
                )
                
        except Exception as e:
            self.logger.error(f"导出文档失败: {e}")
            return ProcessResponse(
                success=False,
                message=f"导出失败: {str(e)}"
            )
    
    def get_document_preview(self, document_path: str) -> ProcessResponse:
        """获取文档预览
        
        Args:
            document_path: 文档路径
            
        Returns:
            处理响应
        """
        try:
            processor = self._get_or_create_processor(document_path)
            preview_text = processor.get_document_text()
            
            return ProcessResponse(
                success=True,
                message="获取预览成功",
                preview_text=preview_text
            )
            
        except Exception as e:
            self.logger.error(f"获取预览失败: {e}")
            return ProcessResponse(
                success=False,
                message=f"获取预览失败: {str(e)}"
            )
    
    def _get_or_create_processor(self, document_path: Optional[str] = None) -> WordProcessor:
        """获取或创建文档处理器
        
        Args:
            document_path: 文档路径
            
        Returns:
            文档处理器
        """
        if document_path:
            # 检查缓存
            if document_path in self.document_cache:
                return self.document_cache[document_path]
            
            # 创建新的处理器
            processor = WordProcessor(document_path)
            self.document_cache[document_path] = processor
            return processor
        else:
            # 创建新文档
            return WordProcessor()
    
    def _generate_output_path(self, original_path: Optional[str] = None) -> str:
        """生成输出文件路径
        
        Args:
            original_path: 原始文件路径
            
        Returns:
            输出文件路径
        """
        if original_path:
            # 基于原始文件生成新路径
            base_name = os.path.splitext(os.path.basename(original_path))[0]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{base_name}_{timestamp}.docx"
        else:
            # 生成新的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"document_{timestamp}.docx"
        
        return os.path.join(self.workspace, filename)
    
    def _generate_document_path(self, title: str) -> str:
        """生成文档路径
        
        Args:
            title: 文档标题
            
        Returns:
            文档路径
        """
        # 清理标题作为文件名
        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_title = clean_title.replace(' ', '_')
        
        if not clean_title:
            clean_title = "untitled"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{clean_title}_{timestamp}.docx"
        
        return os.path.join(self.workspace, filename)
    
    def _generate_export_path(self, source_path: str, export_format: DocumentFormat) -> str:
        """生成导出路径
        
        Args:
            source_path: 源文件路径
            export_format: 导出格式
            
        Returns:
            导出路径
        """
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        extension = export_format.value
        filename = f"{base_name}_export.{extension}"
        
        return os.path.join(self.workspace, filename)
    
    def clear_cache(self):
        """清理文档缓存"""
        self.document_cache.clear()
        self.logger.info("文档缓存已清理")
    
    def get_workspace_files(self) -> List[str]:
        """获取工作区文件列表
        
        Returns:
            文件路径列表
        """
        try:
            files = []
            for filename in os.listdir(self.workspace):
                if filename.endswith('.docx'):
                    files.append(os.path.join(self.workspace, filename))
            return files
        except Exception as e:
            self.logger.error(f"获取工作区文件失败: {e}")
            return []