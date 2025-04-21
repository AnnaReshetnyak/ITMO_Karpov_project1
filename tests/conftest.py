import pytest
from fastapi.testclient import TestClient
from lesson_2.main import app
from lesson_2.app.database.database import get_session, init_db
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from lesson_2.app.database.database import engine



@pytest.fixture(name="db_session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(db_session: Session):
    def get_session_override():
        return db_session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        async with AsyncSession(conn) as session:
            yield session
            await session.rollback()
    await engine.dispose()
