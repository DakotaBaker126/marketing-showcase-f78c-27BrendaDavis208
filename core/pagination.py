from typing import List, TypeVar, Generic
from pydantic import BaseModel, Field
from fastapi import Query


T = TypeVar('T')


class PageParams(BaseModel):
    """
    分页参数模型，用于统一解析查询参数
    支持：page（从1开始）、size（每页数量）、默认值由 config 驱动
    """
    page: int = Field(1, ge=1, description="当前页码（从1开始）")
    size: int = Field(10, ge=1, le=200, description="每页条目数（1-200）")

    @classmethod
    def as_query_params(
        cls,
        page: int = Query(1, ge=1, description="当前页码（从1开始）"),
        size: int = Query(10, ge=1, le=200, description="每页条目数（1-200）"),
    ) -> 'PageParams':
        return cls(page=page, size=size)


class PageResponse(BaseModel, Generic[T]):
    """
    标准化分页响应结构，适配前端交互流畅性要求
    - items: 当前页数据列表
    - total: 总条目数
    - page: 当前页码
    - size: 每页条目数
    - pages: 总页数（向上取整）
    - has_next: 是否有下一页
    - has_prev: 是否有上一页
    """
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool


def paginate_response(
    data: List[T],
    total: int,
    page: int,
    size: int,
) -> PageResponse[T]:
    """
    构造标准化分页响应体
    适用于 mock 数据切片或 DB 查询结果包装，确保前后端分页语义一致、交互反馈明确。
    """
    pages = (total + size - 1) // size if size > 0 else 1
    has_next = page < pages
    has_prev = page > 1

    return PageResponse[
        T  # type: ignore  # Pydantic v2 generic support via runtime param
    ](
        items=data,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=has_next,
        has_prev=has_prev,
    )
