"""应用配置文件"""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""

    # 基础配置
    APP_NAME: str = "Service Shop Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    # 数据库配置
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/wellness_shop"
    SQLALCHEMY_ECHO: bool = False

    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis 配置
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_EXPIRE_SECONDS: int = 300

    # 微信配置
    WECHAT_APP_ID: str = ""
    WECHAT_APP_SECRET: str = ""
    WECHAT_MCH_ID: str = ""
    WECHAT_API_KEY: str = ""
    WECHAT_TOKEN: str = "wellness_shop_token"  # 微信服务器验证token

    # 短信配置（阿里云示例）
    SMS_PROVIDER: str = "aliyun"  # aliyun, tencent, other
    SMS_ACCESS_KEY_ID: str = ""
    SMS_ACCESS_KEY_SECRET: str = ""
    SMS_SIGN_NAME: str = "店铺管理系统"
    SMS_TEMPLATE_CODE: str = ""  # 验证码模板ID

    # CORS 配置
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://yangsheng-game-751fb2.netlify.app",
        "https://nonoccidental-roentgenographic-jordyn.ngrok-free.dev",
    ]

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """获取配置对象（使用缓存）"""
    return Settings()


# 导出全局配置对象
settings = get_settings()
