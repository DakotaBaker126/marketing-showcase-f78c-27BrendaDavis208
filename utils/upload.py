from typing import Optional, Tuple
from fastapi import UploadFile, HTTPException
from pathlib import Path

# 配置常量 minor comment refresh
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB


def validate_upload_file(file: UploadFile) -> Tuple[str, str]:
    """
    校验上传文件：扩展名、大小、内容类型（基础安全检查）
    返回 (mock_file_id, mock_url)
    """
    # 检查文件名与扩展名
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")

    ext = Path(file.filename).suffix.lower().lstrip(".")
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件类型: {ext}。仅支持: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # 检查 Content-Type（宽松匹配）
    content_type = file.content_type or ""
    if ext in ["jpg", "jpeg"] and not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="JPEG 文件 Content-Type 不合法")
    if ext == "png" and not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="PNG 文件 Content-Type 不合法")
    if ext == "pdf" and not content_type.startswith(("application/pdf", "application/octet-stream")):
        raise HTTPException(status_code=400, detail="PDF 文件 Content-Type 不合法")

    # 检查文件大小（读取前先限制流）
    file.file.seek(0, 2)  # 移动到末尾
    size = file.file.tell()
    file.file.seek(0)  # 重置指针
    if size > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"文件过大：{size} 字节，最大允许 {MAX_FILE_SIZE_BYTES} 字节（10 MB）",
        )

    # 生成 mock ID 和 URL（模拟存储后返回可访问路径）
    # 实际集成时可替换为 MinIO / S3 / 本地存储逻辑
    import uuid
    mock_id = str(uuid.uuid4())
    mock_url = f"/api/v1/uploads/mock/{mock_id}.{ext}"

    return mock_id, mock_url


def handle_upload(file: UploadFile) -> dict:
    """
    主上传处理函数：校验 + 返回标准化响应
    返回示例：{"id": "xxx", "url": "/api/v1/uploads/mock/xxx.png", "name": "test.png", "size": 12345}
    """
    mock_id, mock_url = validate_upload_file(file)

    return {
        "id": mock_id,
        "url": mock_url,
        "name": file.filename,
        "size": len(file.file.read()) if hasattr(file.file, 'read') else 0,  # 简化：实际中应避免重复读
        "type": file.content_type or "application/octet-stream",
    }

# 占位：预留异步上传、病毒扫描、元数据提取等扩展钩子
async def async_upload_hook(file_id: str, file: UploadFile) -> None:
    """
    异步后处理钩子（如：生成缩略图、OCR、存入 DB 记录等）
    当前为空实现，供未来扩展。
    """
    pass