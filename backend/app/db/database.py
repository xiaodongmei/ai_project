"""数据库配置和会话管理"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import settings


# 创建异步引擎（使用 SQLite 用于演示）
# 在生产环境中应该使用 postgresql+asyncpg:// 而不是 postgresql://
DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # 内存数据库用于演示

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
    """初始化数据库"""
    async with engine.begin() as conn:
        # 这里会在后续创建模型后调用
        # await conn.run_sync(Base.metadata.create_all)
        pass


async def close_db():
    """关闭数据库"""
    await engine.dispose()
