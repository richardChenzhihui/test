import json
import re
from typing import List, Dict, Any, Optional
from ai.openai_api import OpenAIAPI
from ai.prompt_templates import INSTRUCTION_PARSE_PROMPT
from api.models import WordOperation, OperationType, TextStyle, TableData


class CommandParser:
    """指令解析器"""
    
    def __init__(self, openai_api: OpenAIAPI):
        """初始化指令解析器
        
        Args:
            openai_api: OpenAI API 实例
        """
        self.openai_api = openai_api
    
    def parse_instruction(self, instruction: str, document_content: str = "") -> List[WordOperation]:
        """解析自然语言指令
        
        Args:
            instruction: 自然语言指令
            document_content: 当前文档内容
            
        Returns:
            解析后的操作列表
        """
        try:
            # 使用AI解析指令
            prompt = INSTRUCTION_PARSE_PROMPT.format(
                instruction=instruction,
                document_content=document_content[:1000]  # 限制长度
            )
            
            response = self.openai_api.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # 解析响应
            operations = self._parse_ai_response(response)
            return operations
            
        except Exception as e:
            print(f"解析指令失败: {e}")
            # 回退到简单的关键词解析
            return self._simple_keyword_parse(instruction)
    
    def _parse_ai_response(self, response: str) -> List[WordOperation]:
        """解析AI响应
        
        Args:
            response: AI响应内容
            
        Returns:
            操作列表
        """
        operations = []
        
        try:
            # 提取JSON内容
            json_match = re.search(r'```json\s*(\[.*?\])\s*```', response, re.DOTALL)
            if json_match:
                json_content = json_match.group(1)
            else:
                # 如果没有代码块，尝试直接解析
                json_content = response.strip()
            
            # 解析JSON
            parsed_data = json.loads(json_content)
            
            for item in parsed_data:
                operation = self._create_operation_from_dict(item)
                if operation:
                    operations.append(operation)
                    
        except Exception as e:
            print(f"解析AI响应失败: {e}")
            print(f"响应内容: {response}")
        
        return operations
    
    def _create_operation_from_dict(self, data: Dict[str, Any]) -> Optional[WordOperation]:
        """从字典创建操作对象
        
        Args:
            data: 操作数据字典
            
        Returns:
            操作对象
        """
        try:
            # 验证操作类型
            operation_type = data.get('operation_type')
            if operation_type not in [op.value for op in OperationType]:
                print(f"不支持的操作类型: {operation_type}")
                return None
            
            # 创建样式对象
            style = None
            if 'style' in data and data['style']:
                style_data = data['style']
                style = TextStyle(
                    font_name=style_data.get('font_name'),
                    font_size=style_data.get('font_size'),
                    bold=style_data.get('bold'),
                    italic=style_data.get('italic'),
                    underline=style_data.get('underline'),
                    color=style_data.get('color')
                )
            
            # 创建表格数据对象
            table_data = None
            if 'table_data' in data and data['table_data']:
                table_info = data['table_data']
                table_data = TableData(
                    rows=table_info.get('rows', 1),
                    cols=table_info.get('cols', 1),
                    headers=table_info.get('headers'),
                    data=table_info.get('data')
                )
            
            # 创建操作对象
            operation = WordOperation(
                operation_type=OperationType(operation_type),
                content=data.get('content'),
                position=data.get('position'),
                style=style,
                table_data=table_data,
                metadata=data.get('metadata')
            )
            
            return operation
            
        except Exception as e:
            print(f"创建操作对象失败: {e}")
            return None
    
    def _simple_keyword_parse(self, instruction: str) -> List[WordOperation]:
        """简单的关键词解析（备用方案）
        
        Args:
            instruction: 指令文本
            
        Returns:
            操作列表
        """
        operations = []
        instruction_lower = instruction.lower()
        
        try:
            # 添加文本
            if any(keyword in instruction_lower for keyword in ['添加', '加入', '插入']):
                # 提取要添加的内容
                content = self._extract_content_from_instruction(instruction)
                if content:
                    operations.append(WordOperation(
                        operation_type=OperationType.ADD_TEXT,
                        content=content
                    ))
            
            # 删除文本
            elif any(keyword in instruction_lower for keyword in ['删除', '移除', '去掉']):
                content = self._extract_content_from_instruction(instruction)
                if content:
                    operations.append(WordOperation(
                        operation_type=OperationType.DELETE_TEXT,
                        content=content
                    ))
            
            # 添加标题
            elif any(keyword in instruction_lower for keyword in ['标题', '题目', '章节']):
                content = self._extract_content_from_instruction(instruction)
                level = 1
                if '二级' in instruction_lower or '2级' in instruction_lower:
                    level = 2
                elif '三级' in instruction_lower or '3级' in instruction_lower:
                    level = 3
                
                if content:
                    operations.append(WordOperation(
                        operation_type=OperationType.ADD_HEADING,
                        content=content,
                        metadata={'level': level}
                    ))
            
            # 添加表格
            elif any(keyword in instruction_lower for keyword in ['表格', '表']):
                # 简单的表格解析
                rows = 3
                cols = 2
                if '行' in instruction_lower:
                    rows_match = re.search(r'(\d+)\s*行', instruction_lower)
                    if rows_match:
                        rows = int(rows_match.group(1))
                
                if '列' in instruction_lower:
                    cols_match = re.search(r'(\d+)\s*列', instruction_lower)
                    if cols_match:
                        cols = int(cols_match.group(1))
                
                operations.append(WordOperation(
                    operation_type=OperationType.ADD_TABLE,
                    table_data=TableData(rows=rows, cols=cols)
                ))
            
            # 如果没有匹配到任何操作，默认添加文本
            if not operations:
                operations.append(WordOperation(
                    operation_type=OperationType.ADD_TEXT,
                    content=instruction
                ))
            
        except Exception as e:
            print(f"关键词解析失败: {e}")
        
        return operations
    
    def _extract_content_from_instruction(self, instruction: str) -> str:
        """从指令中提取内容
        
        Args:
            instruction: 指令文本
            
        Returns:
            提取的内容
        """
        # 简单的内容提取逻辑
        # 可以根据需要改进
        patterns = [
            r'["""]([^"""]+)["""]',  # 引号内容
            r'["""]([^"""]+)["""]',  # 中文引号内容
            r'内容[是为][:：]?\s*(.+)',  # "内容是"或"内容为"
            r'添加[:：]?\s*(.+)',  # "添加"
            r'插入[:：]?\s*(.+)',  # "插入"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, instruction)
            if match:
                return match.group(1).strip()
        
        # 如果没有匹配到特定模式，返回整个指令
        return instruction.strip()
    
    def validate_operations(self, operations: List[WordOperation]) -> List[WordOperation]:
        """验证操作列表
        
        Args:
            operations: 操作列表
            
        Returns:
            验证后的操作列表
        """
        valid_operations = []
        
        for operation in operations:
            if self._is_valid_operation(operation):
                valid_operations.append(operation)
            else:
                print(f"无效操作: {operation.operation_type}")
        
        return valid_operations
    
    def _is_valid_operation(self, operation: WordOperation) -> bool:
        """验证单个操作是否有效
        
        Args:
            operation: 操作对象
            
        Returns:
            是否有效
        """
        # 基本验证
        if not operation.operation_type:
            return False
        
        # 根据操作类型验证
        if operation.operation_type in [OperationType.ADD_TEXT, OperationType.DELETE_TEXT, OperationType.ADD_HEADING]:
            return bool(operation.content)
        elif operation.operation_type == OperationType.ADD_TABLE:
            return bool(operation.table_data)
        elif operation.operation_type == OperationType.MODIFY_TEXT:
            return bool(operation.content and operation.metadata and operation.metadata.get('old_text'))
        elif operation.operation_type == OperationType.ADD_LIST:
            return bool(operation.metadata and operation.metadata.get('items'))
        
        return True