from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Local imports
from config import settings
from api import api_router
from core.exceptions import add_exception_handlers
from utils.theme import get_theme_mode


# --- Application Initialization ---
app = FastAPI(
    title="Automation Center",
    description="Lightweight automation task platform prototype (PROMPT-F78CD1-000076)",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)


# --- Middleware ---

class ThemeHeaderMiddleware(BaseHTTPMiddleware):
    """
    Inject current theme mode (light/dark) into response headers for frontend hydration.
    Used to avoid FOUC and enable SSR-like theme sync before JS loads.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        theme_mode = get_theme_mode()
        response.headers["X-Theme-Mode"] = theme_mode
        return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ThemeHeaderMiddleware)


# --- Static Files ---
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- API Routes ---
app.include_router(api_router, prefix="/api/v1")


# --- Exception Handling ---
add_exception_handlers(app)


# --- Health Check Endpoint ---
@app.get("/health", include_in_schema=False)
def health_check():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT,
        "mock_data_enabled": settings.MOCK_DATA_ENABLED,
        "theme_mode": get_theme_mode(),
        "prompt_id": "PROMPT-F78CD1-000076",
    }


# --- Root Redirect ---
@app.get("/", include_in_schema=False)
def root_redirect():
    return {"message": "Automation Center API is running.", "docs": "/docs"}