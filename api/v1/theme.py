from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Literal

from core.exceptions import NotImplementedError
from utils.theme import get_current_theme, set_theme_mode


router = APIRouter(
    prefix="/theme",
    tags=["Theme"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Theme endpoint not found"}},
)


class ThemeResponse(BaseModel):
    mode: Literal["light", "dark"]
    timestamp: float


class ThemeUpdateRequest(BaseModel):
    mode: Literal["light", "dark"]


@router.get("/", response_model=ThemeResponse)
def get_theme():
    """
    获取当前主题模式（light/dark）。
    当前为占位实现，返回静态配置值；未来可对接用户偏好存储或系统级主题策略。
    """
    mode = get_current_theme()
    return ThemeResponse(mode=mode, timestamp=0.0)  # timestamp 保留扩展字段，当前 mock 为 0


@router.put("/", response_model=ThemeResponse)
def update_theme(payload: ThemeUpdateRequest):
    """
    切换主题模式（light/dark）。
    当前为内存占位实现，不持久化；后续可集成数据库、JWT payload 或 localStorage 同步逻辑。
    """
    try:
        set_theme_mode(payload.mode)
        return ThemeResponse(mode=payload.mode, timestamp=0.0)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except NotImplementedError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Theme persistence is not enabled in current configuration.",
        )