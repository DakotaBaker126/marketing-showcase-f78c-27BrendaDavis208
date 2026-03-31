from typing import Generator
from contextlib import contextmanager

# Mock session factory —— placeholder for real SQLAlchemy engine/session setup minor comment refresh
# Retains structure for future DB integration while enabling immediate mock-driven development. minor comment refresh
# PROMPT-F78CD1-000076: This module is intentionally minimal and decoupled from actual DB I/O. minor comment refresh


class MockSession:
    """Lightweight mock session mimicking SQLAlchemy Session interface.
    Supports basic .add(), .commit(), .refresh(), .query() stubs for compatibility with CRUD logic.
    Does NOT persist state — all operations are in-memory and discard on exit.
    """

    def __init__(self):
        self._data = []

    def add(self, instance):
        # In real usage: appends to pending list; here we just store for consistency
        pass

    def commit(self):
        # No-op: mock data lives in core/mock_data.py, not here
        pass

    def refresh(self, instance):
        # No-op: mock objects are plain dicts/Pydantic models
        pass

    def query(self, model):
        # Returns a mock query-like object supporting .filter(), .offset(), .limit(), .all()
        from core.mock_data import get_all_tasks
        from models.task import Task

        class MockQuery:
            def __init__(self, items):
                self.items = items

            def filter(self, *args, **kwargs):
                # Simplified mock filter: only supports status=... for demo clarity
                if len(args) == 1 and hasattr(args[0], 'value') and 'status' in str(args[0]):
                    status_val = getattr(args[0].value, 'value', None) or args[0].value
                    return MockQuery([t for t in self.items if t.get('status') == status_val])
                return self

            def offset(self, n):
                return MockQuery(self.items[n:])

            def limit(self, n):
                return MockQuery(self.items[:n])

            def all(self):
                return [Task(**item) for item in self.items]

        return MockQuery([t.model_dump() if hasattr(t, 'model_dump') else t for t in get_all_tasks()])


@contextmanager
def get_db() -> Generator[MockSession, None, None]:
    """Dependency-injected mock DB session generator.
    Matches FastAPI dependency pattern (yield-based), ready for swap with real AsyncSession later.
    """
    yield MockSession()


# Optional:预留 Engine 初始化占位（uncomment when migrating to real DB）
# from sqlalchemy import create_engine
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from sqlalchemy.orm import sessionmaker
#
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./app.db"  # or env var
#
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
# AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         yield session