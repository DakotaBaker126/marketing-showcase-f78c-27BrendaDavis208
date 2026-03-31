from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from core.exceptions import NotImplementedError
from utils.notify import mark_all_as_read, get_unread_count

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications (Mock)"]
)


class NotificationSummary(BaseModel):
    unread_count: int
    total_count: int = 0  # reserved for future use


class MarkReadRequest(BaseModel):
    ids: Optional[List[int]] = None  # optional list of notification IDs to mark; if empty, mark all


@router.get("/", response_model=NotificationSummary)
def get_notifications_summary():
    """
    GET /notifications — 获取通知摘要（当前仅模拟未读数）
    Returns a lightweight summary with `unread_count`.
    This is a mock endpoint — no real persistence or user context yet.
    """
    try:
        count = get_unread_count()
        return NotificationSummary(unread_count=count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch notifications: {str(e)}")


@router.post("/read", response_model=dict)
def mark_notifications_as_read(payload: MarkReadRequest = None):
    """
    POST /notifications/read — 标记通知为已读（支持全量或指定 ID 列表）
    Payload example:
      {"ids": [101, 102]}  → mark specific
      {} or {"ids": []}     → mark all
    Returns simple confirmation. Mock-only.
    """
    try:
        ids = payload.ids if payload else None
        mark_all_as_read(ids=ids)
        return {"status": "success", "message": "Notifications marked as read"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to mark notifications: {str(e)}")
