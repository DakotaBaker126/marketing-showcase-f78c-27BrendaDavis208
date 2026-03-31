from typing import Literal, Dict, Any

# PROMPT-F78CD1-000076: Theme strategy placeholder — static config only, extensible by design

ThemeMode = Literal["light", "dark"]


def get_theme_config(mode: ThemeMode = "light") -> Dict[str, Any]:
    """
    Returns theme-specific configuration (CSS variables, UI preferences).
    Currently static and mock-driven; designed for seamless future integration
    with persistent user preference storage or dynamic theme engine.
    """
    configs = {
        "light": {
            "name": "light",
            "primary_color": "#4f46e5",
            "background": "#ffffff",
            "surface": "#f9fafb",
            "text_primary": "#111827",
            "text_secondary": "#6b7280",
            "border": "#e5e7eb",
            "success": "#10b981",
            "warning": "#f59e0b",
            "error": "#ef4444",
            "icon_theme": "outline",
        },
        "dark": {
            "name": "dark",
            "primary_color": "#6366f1",
            "background": "#0f172a",
            "surface": "#1e293b",
            "text_primary": "#f1f5f9",
            "text_secondary": "#94a3b8",
            "border": "#334155",
            "success": "#059669",
            "warning": "#d97706",
            "error": "#dc2626",
            "icon_theme": "filled",
        },
    }
    return configs.get(mode, configs["light"])


def validate_theme_mode(mode: str) -> ThemeMode:
    """
    Validates and normalizes theme mode input.
    Ensures safe fallback and consistent typing for downstream use.
    """
    if mode not in ("light", "dark"):
        return "light"
    return mode  # type: ignore