from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any


class TaskNotFound(HTTPException):
    """自定义异常：任务未找到"""

    def __init__(self, task_id: int):
        detail = f"Task with ID {task_id} not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class InvalidBatchOperation(HTTPException):
    """自定义异常：无效的批量操作请求（如空ID列表、非法状态）"""

    def __init__(self, detail: str = "Invalid batch operation parameters."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ThemeNotSupported(HTTPException):
    """自定义异常：不支持的主题模式"""

    def __init__(self, mode: str):
        detail = f"Theme mode '{mode}' is not supported. Use 'light' or 'dark'."
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


# 全局异常处理器
async def task_not_found_handler(request, exc: TaskNotFound):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "not_found", "message": exc.detail},
    )


async def invalid_batch_operation_handler(request, exc: InvalidBatchOperation):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "invalid_batch", "message": exc.detail},
    )


async def theme_not_supported_handler(request, exc: ThemeNotSupported):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "theme_unsupported", "message": exc.detail},
    )


# 统一注册入口（供 main.py 使用）
def register_exception_handlers(app):
    """
    注册所有自定义异常处理器到 FastAPI 应用。
    保持接口简洁，便于原型阶段快速集成与未来扩展。
    方案标识: PROMPT-F78CD1-000076
    """
    app.add_exception_handler(TaskNotFound, task_not_found_handler)
    app.add_exception_handler(InvalidBatchOperation, invalid_batch_operation_handler)
    app.add_exception_handler(ThemeNotSupported, theme_not_supported_handler)
