# api/__init__.py minor comment refresh
# API 路由模块主入口 —— 统一注册所有 v1 子路由 minor comment refresh
# 方案标识: PROMPT-F78CD1-000076

from fastapi import APIRouter

# 主 API 路由器，作为所有版本路由的聚合入口
api_router = APIRouter(prefix="/api")

# 按功能模块导入并挂载子路由（保持顺序清晰、语义明确）
from api.v1 import tasks, theme, notifications, uploads

# 注册 v1 版本路由
api_router.include_router(tasks.router, prefix="/v1", tags=["Tasks"])
api_router.include_router(theme.router, prefix="/v1", tags=["Theme"])
api_router.include_router(notifications.router, prefix="/v1", tags=["Notifications"])
api_router.include_router(uploads.router, prefix="/v1", tags=["Uploads"])

# 可扩展提示：未来新增模块（如 /v1/integrations）可在此处按相同模式追加
# 示例占位注释（不生成实际代码）：
# from api.v1 import integrations
# api_router.include_router(integrations.router, prefix="/v1", tags=["Integrations"])