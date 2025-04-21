import pytest
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from lesson_2.app.database.services.crud.user_crud import UserCRUD
from lesson_2.app.exceptions import DuplicateEmailError
from lesson_2.app.models import User
from lesson_2.app.schemas import UserCreate


@pytest.fixture
async def async_session():
    engine = create_engine("sqlite:///:memory:", echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    return AsyncSession(engine)


@pytest.mark.asyncio
async def test_user_creation(async_session):
    user_data = UserCreate(email="test@example.com", password="password")
    crud = UserCRUD(async_session)

    user = await crud.create(user_data)

    assert user.email == "test@example.com"
    assert user.hashed_password is not None
    assert user.is_active is True
    assert user.is_admin is False
