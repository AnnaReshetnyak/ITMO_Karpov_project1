import pytest
from fastapi.testclient import TestClient

from lesson_2.app.database.services.crud.user_crud import UserCRUD
from lesson_2.main import app
from lesson_2.app.database.database import get_session, init_db
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from lesson_2.app.database.database import engine
from lesson_2.app.database.models import User, Balance, MLModel

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    import os
    os.environ["ENVIRONMENT"] = "TEST"
    os.environ["DATABASE_URL"] = "sqlite:///test.db"


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


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)


@pytest.fixture(scope="session")
async def db_engine():
    engine = create_engine("sqlite:///:memory:", echo=True)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="module", autouse=True)
def init():
    init_db()


@pytest.fixture
async def db_session(db_engine):
    async with AsyncSession(db_engine) as session:
        yield session
        await session.rollback()


@pytest.fixture
async def test_user(db_session):
    user = User(email="test@example.com", hashed_password="hashed")
    db_session.add(user)
    await db_session.commit()
    return user


@pytest.fixture
async def test_balance(db_session, test_user):
    balance = Balance(user_id=test_user.id, amount=100.0)
    db_session.add(balance)
    await db_session.commit()
    return balance


@pytest.fixture
async def auth_headers(test_client, db_session):
    user_data = {"email": "authuser@example.com", "password": "password"}
    crud = UserCRUD(db_session)
    await crud.create(user_data)

    response = test_client.post(
        "/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]}
    )
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def test_ml_model(db_session):
    model = MLModel(name="Test Model", version="1.0")
    db_session.add(model)
    await db_session.commit()
    return model
