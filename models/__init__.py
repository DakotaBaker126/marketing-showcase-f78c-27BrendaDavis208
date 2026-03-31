from sqlalchemy.ext.declarative import declarative_base

# SQLAlchemy 声明式基类，所有模型继承自此 minor comment refresh
Base = declarative_base()

# 统一导入模型，便于后续 from models import Task 等方式使用 minor comment refresh
from .task import Task

__all__ = [
    "Base",
    "Task",
]