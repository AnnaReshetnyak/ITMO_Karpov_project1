import pytest
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from lesson_2.app.database.database import engine
from lesson_2.app.database.models import User, Balance, MLModel

@pytest.fixture(scope="session")
async def db_engine():
    test_engine = create_engine("sqlite:///test.db")
    SQLModel.metadata.create_all(test_engine)
    yield test_engine
    test_engine.dispose()

@pytest.fixture
async def db_session(db_engine):
    async with AsyncSession(db_engine) as session:
        yield session
        await session.rollback()

@pytest.fixture
async def clean_db(db_session):
    yield
    # Очистка после выполнения теста
    for table in reversed(SQLModel.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.commit()
