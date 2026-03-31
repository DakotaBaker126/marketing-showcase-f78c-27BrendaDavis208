from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import random

# PROMPT-F78CD1-000076: Mock data source for rapid prototyping.
# Preloaded with 24 realistic task samples; supports filtering, pagination, and deterministic refresh.

# Task status options
STATUSES = ["pending", "running", "completed", "failed", "cancelled"]

# Predefined mock tasks (24 entries — ensures robust pagination testing)
MOCK_TASKS = [
    {
        "id": 1,
        "title": "Initialize CI/CD pipeline",
        "status": "completed",
        "created_at": (datetime.now() - timedelta(days=12, hours=3)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=11, hours=8)).isoformat(),
        "description": "Configure GitHub Actions for automated testing and deployment."
    },
    {
        "id": 2,
        "title": "Sync user preferences across devices",
        "status": "running",
        "created_at": (datetime.now() - timedelta(days=10, minutes=17)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=10, minutes=5)).isoformat(),
        "description": "Implement encrypted sync via WebDAV backend."
    },
    {
        "id": 3,
        "title": "Audit third-party API permissions",
        "status": "pending",
        "created_at": (datetime.now() - timedelta(days=9, hours=14)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=9, hours=14)).isoformat(),
        "description": "Review OAuth scopes and revoke unused grants."
    },
    {
        "id": 4,
        "title": "Generate quarterly usage report",
        "status": "completed",
        "created_at": (datetime.now() - timedelta(days=8, hours=22)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=8, hours=20)).isoformat(),
        "description": "Aggregate analytics from telemetry endpoints."
    },
    {
        "id": 5,
        "title": "Migrate legacy config to YAML schema",
        "status": "failed",
        "created_at": (datetime.now() - timedelta(days=7, hours=5)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=7, hours=2)).isoformat(),
        "description": "Validation failed on nested array constraints."
    },
    {
        "id": 6,
        "title": "Validate dark mode contrast ratios",
        "status": "completed",
        "created_at": (datetime.now() - timedelta(days=6, hours=18)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=6, hours=16)).isoformat(),
        "description": "Ensure WCAG AA compliance for all interactive elements."
    },
    {
        "id": 7,
        "title": "Back up production database snapshot",
        "status": "running",
        "created_at": (datetime.now() - timedelta(days=5, hours=9)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=5, hours=7)).isoformat(),
        "description": "Compressed pg_dump to S3 with versioned tagging."
    },
    {
        "id": 8,
        "title": "Update dependency licenses inventory",
        "status": "pending",
        "created_at": (datetime.now() - timedelta(days=4, hours=13)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=4, hours=13)).isoformat(),
        "description": "Cross-check SPDX identifiers against latest scan results."
    },
    {
        "id": 9,
        "title": "Test notification delivery fallback path",
        "status": "completed",
        "created_at": (datetime.now() - timedelta(days=3, hours=2)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=3, hours=1)).isoformat(),
        "description": "Simulate email/SMS gateway failure and verify push recovery."
    },
    {
        "id": 10,
        "title": "Refactor task scheduler concurrency model",
        "status": "failed",
        "created_at": (datetime.now() - timedelta(days=2, hours=11)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=2, hours=9)).isoformat(),
        "description": "Race condition observed under >500 concurrent jobs."
    },
    {
        "id": 11,
        "title": "Verify file upload size limits in staging",
        "status": "pending",
        "created_at": (datetime.now() - timedelta(days=1, hours=16)).isoformat(),
        "updated_at": (datetime.now() - timedelta(days=1, hours=16)).isoformat(),
        "description": "Confirm 128MB cap enforcement and client-side feedback."
    },
    {
        "id": 12,
        "title": "Run accessibility audit on dashboard widgets",
        "status": "completed",
        "created_at": (datetime.now() - timedelta(hours=22)).isoformat(),
        "updated_at": (datetime.now() - timedelta(hours=20)).isoformat(),
        "description": "axe-core scan + manual keyboard navigation validation."
    },
    {
        "id": 13,
        "title": "Refresh OAuth token rotation policy",
        "status": "running",
        "created_at": (datetime.now() - timedelta(hours=15)).isoformat(),
        "updated_at": (datetime.now() - timedelta(hours=13)).isoformat(),
        "description": "Extend short-lived tokens and update refresh logic."
    },
    {
        "id": 14,
        "title": "Sanitize user-uploaded HTML content",
        "status": "pending",
        "created_at": (datetime.now() - timedelta(hours=8)).isoformat(),
        "updated_at": (datetime.now() - timedelta(hours=8)).isoformat(),
        "description": "Integrate DOMPurify with custom allow-list for rich text."
    },
    {
        "id": 15,
        "title": "Deploy theme-aware icon set",
        "status": "completed",
        "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
        "updated_at": (datetime.now() - timedelta(minutes=45)).isoformat(),
        "description": "SVG icons with CSS variable-based fill/stroke."
    },
    {
        "id": 16,
        "title": "Stress-test batch task update endpoint",
        "status": "failed",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "description": "500+ updates triggered timeout; investigate transaction isolation."
    },
    {
        "id": 17,
        "title": "Validate timezone-aware scheduling logic",
        "status": "running",
        "created_at": (datetime.now() + timedelta(minutes=5)).isoformat(),
        "updated_at": (datetime.now() + timedelta(minutes=3)).isoformat(),
        "description": "Confirm cron expressions respect user's IANA zone."
    },
    {
        "id": 18,
        "title": "Benchmark SQLite → PostgreSQL migration path",
        "status": "pending",
        "created_at": (datetime.now() + timedelta(minutes=12)).isoformat(),
        "updated_at": (datetime.now() + timedelta(minutes=12)).isoformat(),
        "description": "Measure overhead of async session binding and connection pooling."
    },
    {
        "id": 19,
        "title": "Add retry logic to external webhook calls",
        "status": "completed",
        "created_at": (datetime.now() + timedelta(minutes=20)).isoformat(),
        "updated_at": (datetime.now() + timedelta(minutes=18)).isoformat(),
        "description": "Exponential backoff with jitter for HTTP 429/5xx."
    },
    {
        "id": 20,
        "title": "Document mock data generation strategy",
        "status": "pending",
        "created_at": (datetime.now() + timedelta(minutes=27)).isoformat(),
        "updated_at": (datetime.now() + timedelta(minutes=27)).isoformat(),
        "description": "Capture rules for determinism, realism, and extensibility."
    },
    {
        "id": 21,
        "title": "Profile memory usage during long-running tasks",
        "status": "running",
        "created_at": (datetime.now() + timedelta(minutes=35)).isoformat(),
        "updated_at": (datetime.now() + timedelta(minutes=33)).isoformat(),
        "description": "Track object retention and garbage collection triggers."
    },
    {
        "id": 22,
        "title": "Validate CSP headers for embedded iframe sources",
        "status": "completed",
        "created_at": (datetime.now() + timedelta(minutes=42)).isoformat(),
        "updated_at": (datetime.now() + timedelta(minutes=40)).isoformat(),
        "description": "Ensure safe sandboxing without breaking analytics."
    },
    {
        "id": 23,
        "title": "Test offline-first task queue persistence",
        "status": "pending",
        "created_at": (datetime.now() + timedelta(minutes=50)).isoformat(),
        "updated_at": (datetime.now() + timedelta(minutes=50)).isoformat(),
        "description": "IndexedDB fallback with conflict resolution hints."
    },
    {
        "id": 24,
        "title": "Audit all hardcoded strings for i18n readiness",
        "status": "completed",
        "created_at": (datetime.now() + timedelta(minutes=58)).isoformat(),
        "updated_at": (datetime.now() + timedelta(minutes=56)).isoformat(),
        "description": "Extract keys, verify interpolation safety, add context comments."
    },
]


def get_all_tasks() -> List[Dict[str, Any]]:
    """Return full immutable list of mock tasks. Deterministic order for consistent pagination."""
    return MOCK_TASKS.copy()


def filter_tasks(
    tasks: List[Dict[str, Any]], 
    status: Optional[str] = None,
    search: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter tasks by status and/or substring match in title or description.
    Case-insensitive, whitespace-normalized.
    """
    filtered = tasks
    if status and status in STATUSES:
        filtered = [t for t in filtered if t["status"] == status]
    if search:
        search_lower = search.strip().lower()
        if search_lower:
            filtered = [
                t for t in filtered
                if search_lower in t["title"].lower() or 
                   search_lower in t.get("description", "").lower()
            ]
    return filtered


def paginate_tasks(
    tasks: List[Dict[str, Any]], 
    page: int = 1, 
    size: int = 10
) -> Dict[str, Any]:
    """
    Slice tasks into page chunks. Returns dict with 'items', 'page', 'size', 'total'.
    Ensures page >= 1, size between 1–100.
    """
    page = max(1, page)
    size = max(1, min(100, size))
    start = (page - 1) * size
    end = start + size
    paginated = tasks[start:end]
    total = len(tasks)

    return {
        "items": paginated,
        "page": page,
        "size": size,
        "total": total,
        "pages": (total + size - 1) // size  # ceil division
    }


def refresh_mock_data(seed: Optional[int] = None) -> None:
    """
    (Optional) Reset/mock data state — currently no-op since MOCK_TASKS is static.
    Reserved for future extensions: randomized timestamps, synthetic status churn, etc.
    If seed provided, enables reproducible shuffling (e.g., for demo replay).
    """
    if seed is not None:
        # In future: shuffle with seed, regenerate dynamic fields
        pass

# Export for direct use in API handlers
__all__ = [
    "get_all_tasks",
    "filter_tasks",
    "paginate_tasks",
    "refresh_mock_data",
    "STATUSES",
]
