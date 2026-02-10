"""数据库配置和会话管理"""
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.db.base import Base
# 导入所有模型，确保它们注册到 Base.metadata
import app.models  # noqa: F401


# 判断数据库 URL 类型
_raw_url = os.environ.get("DATABASE_URL", settings.DATABASE_URL)

if _raw_url.startswith("postgresql://"):
    # Docker/生产环境：使用 PostgreSQL (asyncpg)
    DATABASE_URL = _raw_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    engine = create_async_engine(
        DATABASE_URL,
        echo=settings.SQLALCHEMY_ECHO,
        future=True,
        pool_size=5,
        max_overflow=10,
    )
else:
    # 本地开发/回退：使用 SQLite 文件持久化
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "wellness.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(
        DATABASE_URL,
        echo=settings.SQLALCHEMY_ECHO,
        future=True,
        connect_args={"check_same_thread": False},
    )

# 创建异步会话工厂
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """获取数据库会话（依赖注入）"""
    async with async_session() as session:
        yield session


async def init_db():
    """初始化数据库 - 自动创建所有表（多worker安全）"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        # 多worker启动时可能出现竞争条件，忽略重复创建错误
        import logging
        logging.getLogger(__name__).warning(f"init_db warning (safe to ignore if tables exist): {e}")


async def close_db():
    """关闭数据库"""
    await engine.dispose()
