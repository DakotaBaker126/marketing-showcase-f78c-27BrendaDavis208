# automation-center-f78c-24TaylorSmith575

> **A lightweight, demo-ready automation task platform prototype**
> Built with FastAPI + SQLAlchemy • Mock-driven • UX-optimized • Extensible-by-design

---

## 🌟 Overview

`automation-center-f78c-24TaylorSmith575` is a production-intent prototype for an intuitive automation task center — designed for rapid demonstration, stakeholder review, and seamless prototype-to-MVP transition. It delivers polished frontend interaction (via mock data) while maintaining clean, modular, and well-annotated backend architecture. All core capabilities are implemented or explicitly *reserved as functional placeholders* — including theme switching, notifications, and file uploads — ensuring zero architectural debt at launch.

✅ **Solution Identifier**: `PROMPT-F78CD1-000076` — *This exact identifier appears in config, logs, and docs to guarantee traceability across variants.*

---

## ⚙️ Quick Start

### Prerequisites
- Python 3.10+
- `pip` (≥22.0)
- Optional: `uvicorn` (auto-installed via `requirements.txt`)

### Setup & Run
```bash
# 1. Clone & enter project
git clone <repo-url> && cd automation-center-f78c-24TaylorSmith575

# 2. Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment (optional customization)
cp .env .env.local
# → edit .env.local to adjust DEBUG, MOCK_DATA_ENABLED, etc.

# 5. Launch server
uvicorn main:app --reload --host 0.0.0.0:8000
```

✅ API docs auto-available at: [`http://localhost:8000/docs`](http://localhost:8000/docs)  
✅ ReDoc at: [`http://localhost:8000/redoc`](http://localhost:8000/redoc)

---

## 📋 Core Features

| Feature | Status | Notes |
|--------|--------|-------|
| ✅ RESTful Task CRUD (v1) | Implemented | Full Pydantic validation, idempotent batch update (`PUT /tasks/batch`) |
| ✅ Pagination (`limit`/`offset`, default 10) | Implemented | Consistent `TaskPageResponse` schema; supports `?status=running` filtering |
| ✅ Mock Data Engine | Enabled by default | 24+ realistic tasks in `core/mock_data.py`; refreshable via `/api/v1/tasks/refresh` (dev-only) |
| ✅ Theme Switching (`light`/`dark`) | Placeholder API + CSS vars | `GET/PUT /api/v1/theme`; `static/css/main.css` defines both palettes |
| ✅ Notification Module | Placeholder API only | `GET /notifications` returns `{"unread": 3}`; `POST /notifications/read` is no-op stub |
| ✅ File Upload Endpoint | Placeholder w/ validation | `POST /api/v1/uploads`: accepts `multipart/form-data`, validates type/size, returns mock `file_id` & URL |
| ✅ Structured Error Handling | Implemented | Custom `TaskNotFound`, global JSON error responses |
| ✅ Configurable Defaults | Via `config.py` & `.env` | Toggle `MOCK_DATA_ENABLED`, set `PAGE_DEFAULT_LIMIT`, `THEME_DEFAULT_MODE`, etc. |

---

## 🧱 Architecture Highlights

- **Modular Design**: Strict separation of `models`, `schemas`, `api`, `core`, `utils` — no cross-layer leakage.
- **Zero DB Lock-in**: `core/database.py` exports a `get_db()` session factory that currently yields mock data — ready to swap in real SQLAlchemy engine.
- **Frontend-Ready APIs**: All endpoints return consistent, documented schemas; pagination response includes `total`, `page`, `limit`, `items`.
- **Production-Ready Defaults**: CORS enabled, request ID middleware, structured logging stubs included.
- **Extensibility First**: Every placeholder (theme, notify, upload) exposes clear extension points — e.g., `utils/theme.py` uses strategy pattern stubs.

---

## 📄 License

MIT — Free to use, modify, and deploy for prototyping and internal evaluation.

---

> 🛠️ Maintained under variant specification **`PROMPT-F78CD1-000076`** — *All generated artifacts (code, config, docs) embed this tag for unambiguous version lineage.*