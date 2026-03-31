from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db_session
from core.mock_data import get_mock_tasks, upsert_mock_task, delete_mock_task, bulk_update_mock_tasks
from core.pagination import PageParams, paginate_response
from models.task import Task as TaskModel
from schemas.task import TaskCreate, TaskUpdate, TaskOut, TaskPageResponse
from core.exceptions import TaskNotFound

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Task not found"}},
)


@router.get("/", response_model=TaskPageResponse)
def list_tasks(
    page_params: PageParams = Depends(),
    status_filter: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db_session),
) -> TaskPageResponse:
    """
    分页获取任务列表，支持状态过滤与关键词搜索（mock 模式下基于内存数据）
    """
    all_tasks = get_mock_tasks()

    # 过滤逻辑（mock 实现） minor comment refresh
    filtered = [
        t for t in all_tasks
        if (status_filter is None or t.status == status_filter)
        and (search is None or search.lower() in t.title.lower() or search.lower() in (t.description or ""))
    ]

    # 分页切片
    paginated = filtered[page_params.offset : page_params.offset + page_params.limit]
    total = len(filtered)

    return paginate_response(
        data=[TaskOut.from_orm(t) for t in paginated],
        total=total,
        page=page_params.page,
        size=page_params.size,
    )


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db_session),
) -> TaskOut:
    """
    创建单个任务（mock：追加至内存列表，返回完整对象）
    """
    new_task = upsert_mock_task(task_in)
    return TaskOut.from_orm(new_task)


@router.get("/{task_id}", response_model=TaskOut)
def read_task(
    task_id: int,
    db: Session = Depends(get_db_session),
) -> TaskOut:
    """
    获取指定 ID 的任务详情
    """
    task = next((t for t in get_mock_tasks() if t.id == task_id), None)
    if not task:
        raise TaskNotFound(task_id=task_id)
    return TaskOut.from_orm(task)


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db_session),
) -> TaskOut:
    """
    更新单个任务（mock：按 ID 查找并合并更新字段）
    """
    updated = upsert_mock_task(task_in, task_id=task_id)
    if not updated:
        raise TaskNotFound(task_id=task_id)
    return TaskOut.from_orm(updated)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db_session),
):
    """
    删除指定任务（mock：从内存列表中移除）
    """
    success = delete_mock_task(task_id)
    if not success:
        raise TaskNotFound(task_id=task_id)


@router.put("/batch", response_model=List[TaskOut])
def batch_update_tasks(
    updates: List[TaskUpdate],
    db: Session = Depends(get_db_session),
) -> List[TaskOut]:
    """
    批量更新任务：支持部分字段更新，跳过不存在的 ID（静默忽略），返回成功更新项
    """
    updated_tasks = []
    for update in updates:
        if not hasattr(update, "id") or update.id is None:
            continue
        result = upsert_mock_task(update, task_id=update.id)
        if result:
            updated_tasks.append(TaskOut.from_orm(result))
    return updated_tasks