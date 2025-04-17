from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from lesson_2.app.database.config import get_settings
from sqlalchemy.orm import sessionmaker, declarative_base

# Настройка асинхронного движка
engine = create_engine(
    get_settings.DATABASE_URL,
    echo=True,
    future=True
)

# Асинхронная сессия
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

