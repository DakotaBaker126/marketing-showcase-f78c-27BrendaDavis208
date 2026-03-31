from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """任务基础字段，供继承使用"""
    title: str = Field(..., min_length=1, max_length=128, description="任务标题")
    description: Optional[str] = Field(None, max_length=512, description="任务描述")
    status: str = Field("pending", pattern=r"^(pending|running|completed|failed|canceled)$", description="任务状态")


class TaskCreate(TaskBase):
    """创建任务的请求 Schema"""
    pass


class TaskUpdate(BaseModel):
    """更新任务的请求 Schema（全部字段可选）"""
    title: Optional[str] = Field(None, min_length=1, max_length=128)
    description: Optional[str] = Field(None, max_length=512)
    status: Optional[str] = Field(None, pattern=r"^(pending|running|completed|failed|canceled)$")


class TaskOut(TaskBase):
    """任务详情响应 Schema（含数据库 ID 和时间戳）"""
    id: int = Field(..., description="任务唯一标识符")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="最后更新时间")

    class Config:
        orm_mode = True


class TaskPageResponse(BaseModel):
    """分页任务列表响应 Schema"""
    items: List[TaskOut] = Field(..., description="当前页任务列表")
    total: int = Field(..., description="总任务数")
    page: int = Field(..., ge=1, description="当前页码")
    page_size: int = Field(..., ge=1, le=100, description="每页数量")
    pages: int = Field(..., ge=0, description="总页数（向下取整）")
# minor comment refresh