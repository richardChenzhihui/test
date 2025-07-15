from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import shutil
import tempfile
from pathlib import Path

from word_agent.agent_engine import WordAgent
from api.models import (
    ProcessRequest, ProcessResponse, 
    CreateDocumentRequest, ExportRequest,
    DocumentFormat
)
from config import load_config
from utils.logger import setup_logger

# 创建 FastAPI 应用
app = FastAPI(
    title="Word Agent API",
    description="基于 AI 的 Word 文档智能编辑服务",
    version="1.0.0"
)

# 全局变量
word_agent: Optional[WordAgent] = None
logger = setup_logger()

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    global word_agent
    try:
        config = load_config()
        word_agent = WordAgent(config)
        logger.info("Word Agent 服务启动成功")
    except Exception as e:
        logger.error(f"Word Agent 服务启动失败: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    global word_agent
    if word_agent:
        word_agent.clear_cache()
        logger.info("Word Agent 服务关闭")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Word Agent API 服务正在运行",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/api/word/process", response_model=ProcessResponse)
async def process_document(request: ProcessRequest):
    """处理文档编辑指令
    
    Args:
        request: 处理请求
        
    Returns:
        处理响应
    """
    try:
        if not word_agent:
            raise HTTPException(status_code=500, detail="Word Agent 未初始化")
        
        response = word_agent.process_instruction(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"处理文档失败: {e}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@app.post("/api/word/create", response_model=ProcessResponse)
async def create_document(request: CreateDocumentRequest):
    """创建新文档
    
    Args:
        request: 创建文档请求
        
    Returns:
        处理响应
    """
    try:
        if not word_agent:
            raise HTTPException(status_code=500, detail="Word Agent 未初始化")
        
        response = word_agent.create_document(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建文档失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建失败: {str(e)}")

@app.get("/api/word/preview", response_model=ProcessResponse)
async def get_document_preview(document_path: str):
    """获取文档预览
    
    Args:
        document_path: 文档路径
        
    Returns:
        处理响应
    """
    try:
        if not word_agent:
            raise HTTPException(status_code=500, detail="Word Agent 未初始化")
        
        response = word_agent.get_document_preview(document_path)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取预览失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取预览失败: {str(e)}")

@app.post("/api/word/export", response_model=ProcessResponse)
async def export_document(request: ExportRequest):
    """导出文档
    
    Args:
        request: 导出请求
        
    Returns:
        处理响应
    """
    try:
        if not word_agent:
            raise HTTPException(status_code=500, detail="Word Agent 未初始化")
        
        response = word_agent.export_document(request)
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.message)
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"导出文档失败: {e}")
        raise HTTPException(status_code=500, detail=f"导出失败: {str(e)}")

@app.get("/api/word/download/{filename}")
async def download_document(filename: str):
    """下载文档
    
    Args:
        filename: 文件名
        
    Returns:
        文件响应
    """
    try:
        if not word_agent:
            raise HTTPException(status_code=500, detail="Word Agent 未初始化")
        
        # 检查文件是否在工作区中
        workspace_files = word_agent.get_workspace_files()
        file_path = None
        
        for file in workspace_files:
            if os.path.basename(file) == filename:
                file_path = file
                break
        
        if not file_path or not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="文件不存在")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"下载文档失败: {e}")
        raise HTTPException(status_code=500, detail=f"下载失败: {str(e)}")

@app.post("/api/word/upload")
async def upload_document(file: UploadFile = File(...)):
    """上传文档
    
    Args:
        file: 上传的文件
        
    Returns:
        上传结果
    """
    try:
        if not word_agent:
            raise HTTPException(status_code=500, detail="Word Agent 未初始化")
        
        # 检查文件格式
        if not file.filename.endswith('.docx'):
            raise HTTPException(status_code=400, detail="只支持 .docx 格式文件")
        
        # 保存文件到工作区
        upload_path = os.path.join(word_agent.workspace, file.filename)
        
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return {
            "success": True,
            "message": "文件上传成功",
            "file_path": upload_path,
            "filename": file.filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"上传文档失败: {e}")
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")

@app.get("/api/word/files")
async def list_workspace_files():
    """获取工作区文件列表
    
    Returns:
        文件列表
    """
    try:
        if not word_agent:
            raise HTTPException(status_code=500, detail="Word Agent 未初始化")
        
        files = word_agent.get_workspace_files()
        file_list = []
        
        for file_path in files:
            file_info = {
                "filename": os.path.basename(file_path),
                "path": file_path,
                "size": os.path.getsize(file_path),
                "modified": os.path.getmtime(file_path)
            }
            file_list.append(file_info)
        
        return {
            "success": True,
            "files": file_list,
            "total": len(file_list)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取文件列表失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取文件列表失败: {str(e)}")

@app.delete("/api/word/files/{filename}")
async def delete_document(filename: str):
    """删除文档
    
    Args:
        filename: 文件名
        
    Returns:
        删除结果
    """
    try:
        if not word_agent:
            raise HTTPException(status_code=500, detail="Word Agent 未初始化")
        
        file_path = os.path.join(word_agent.workspace, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="文件不存在")
        
        os.remove(file_path)
        
        return {
            "success": True,
            "message": "文件删除成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除文档失败: {e}")
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

@app.post("/api/word/clear-cache")
async def clear_cache():
    """清理缓存
    
    Returns:
        清理结果
    """
    try:
        if not word_agent:
            raise HTTPException(status_code=500, detail="Word Agent 未初始化")
        
        word_agent.clear_cache()
        
        return {
            "success": True,
            "message": "缓存清理成功"
        }
        
    except Exception as e:
        logger.error(f"清理缓存失败: {e}")
        raise HTTPException(status_code=500, detail=f"清理缓存失败: {str(e)}")

@app.get("/api/health")
async def health_check():
    """健康检查
    
    Returns:
        健康状态
    """
    try:
        if not word_agent:
            return {
                "status": "unhealthy",
                "message": "Word Agent 未初始化"
            }
        
        return {
            "status": "healthy",
            "message": "服务正常运行",
            "workspace": word_agent.workspace,
            "cache_size": len(word_agent.document_cache)
        }
        
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return {
            "status": "unhealthy",
            "message": f"服务异常: {str(e)}"
        }

# 错误处理
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Not Found",
        "message": "请求的资源不存在",
        "status_code": 404
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    logger.error(f"内部服务器错误: {exc}")
    return {
        "error": "Internal Server Error",
        "message": "内部服务器错误",
        "status_code": 500
    }