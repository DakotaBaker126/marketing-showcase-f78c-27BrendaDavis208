from fastapi import APIRouter

# v1 版本路由命名空间入口
# 所有 /api/v1/ 下的子路由在此统一挂载
# 方案标识：PROMPT-F78CD1-000076

router = APIRouter(prefix="/v1", tags=["v1"])

# 按功能模块导入并挂载子路由
from . import tasks, theme, notifications, uploads

router.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
router.include_router(theme.router, prefix="/theme", tags=["Theme"])
router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
router.include_router(uploads.router, prefix="/uploads", tags=["Uploads"])

# 可扩展：未来可添加 /v1/integrations、/v1/schedules 等
# 当前保持轻量，聚焦核心占位能力与 mock 驱动体验