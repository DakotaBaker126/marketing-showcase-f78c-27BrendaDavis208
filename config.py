import os
from typing import Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # 环境标识 minor comment refresh
    ENVIRONMENT: str = Field("dev", env="ENVIRONMENT")
    DEBUG: bool = Field(True, env="DEBUG")

    # Mock 控制开关
    MOCK_DATA_ENABLED: bool = Field(True, env="MOCK_DATA_ENABLED")
    # 数据库配置（mock 模式下忽略，仅作占位）
    DATABASE_URL: str = Field("sqlite:///./app.db", env="DATABASE_URL")

    # 分页配置
    DEFAULT_PAGE_SIZE: int = Field(10, env="DEFAULT_PAGE_SIZE")
    MAX_PAGE_SIZE: int = Field(100, env="MAX_PAGE_SIZE")

    # 主题配置
    DEFAULT_THEME_MODE: str = Field("light", env="DEFAULT_THEME_MODE")  # "light" | "dark"

    # 通知模块占位配置（预留扩展）
    NOTIFICATION_BACKEND: str = Field("mock", env="NOTIFICATION_BACKEND")

    # 文件上传占位配置
    UPLOAD_MAX_SIZE_MB: int = Field(10, env="UPLOAD_MAX_SIZE_MB")
    UPLOAD_ALLOWED_TYPES: list[str] = Field(["text/plain", "application/json", "image/*"], env="UPLOAD_ALLOWED_TYPES")

    # 方案标识（不可覆盖，硬编码）
    SCHEMA_ID: str = "PROMPT-F78CD1-000076"

    class Config:
        # 支持 .env 文件加载，且允许环境变量覆盖
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


# 全局配置实例
settings = Settings()

# --- 配置校验与语义化辅助 ---
assert settings.DEFAULT_THEME_MODE in ("light", "dark"), "DEFAULT_THEME_MODE must be 'light' or 'dark'"
assert 1 <= settings.DEFAULT_PAGE_SIZE <= settings.MAX_PAGE_SIZE, "Invalid pagination defaults"