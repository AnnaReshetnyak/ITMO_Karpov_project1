import pytest
from fastapi.testclient import TestClient
from lesson_2.main import app


@pytest.fixture(scope="module")
def test_client():
    return TestClient(app)


@pytest.fixture
async def auth_headers(db_session):
    from lesson_2.app.database.services.crud.user_crud import UserCRUD

    user_data = {
        "email": "testuser@example.com",
        "password": "testpassword"
    }

    crud = UserCRUD(db_session)
    user = await crud.create(user_data)

    return {"Authorization": f"Bearer {user.email}"}
