from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from utils.upload import handle_upload_mock

router = APIRouter(
    prefix="/v1",
    tags=["uploads"],
    responses={404: {"description": "Not found"}},
)


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    content_type: str
    url: str  # mock CDN-like URL


@router.post("/uploads", response_model=UploadResponse)
async def upload_file(
    file: UploadFile = File(...),
):
    """
    文件上传占位接口（mock 模式）。
    接收 multipart/form-data，校验基础字段（size ≤ 10MB, 支持常见类型），
    返回模拟文件元数据及可访问的 mock URL。
    保留未来对接 MinIO/OSS/S3 的扩展钩子。
    """
    try:
        return await handle_upload_mock(file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Upload failed unexpectedly")
# minor comment refresh
# minor comment refresh