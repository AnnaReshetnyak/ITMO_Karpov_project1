import pytest
from fastapi import status
from sqlmodel import select
from database.models import User
from schemas import UserCreate


@pytest.mark.asyncio
class TestAuthFlow:
    async def test_successful_registration(self, test_client, db_session):
        # Тест успешной регистрации
        user_data = {
            "email": "new.user@example.com",
            "password": "Str0ngP@ss!"
        }

        response = test_client.post("/auth/register", json=user_data)
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()

        # Проверка записи в БД
        user = await db_session.execute(select(User).where(User.email == user_data["email"]))
        assert user.scalar_one_or_none() is not None

    async def test_duplicate_registration(self, test_client, test_user):
        # Тест регистрации с существующим email
        response = test_client.post(
            "/auth/register",
            json={"email": test_user.email, "password": "anypassword"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"].lower()

    async def test_successful_login(self, test_client, test_user):
        # Тест успешного входа
        response = test_client.post(
            "/auth/login",
            data={"username": test_user.email, "password": "testpassword"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()

    async def test_invalid_credentials(self, test_client, test_user):
        # Тест неверных учетных данных
        test_cases = [
            {"username": test_user.email, "password": "wrongpassword"},
            {"username": "nonexistent@example.com", "password": "anypassword"}
        ]

        for case in test_cases:
            response = test_client.post("/auth/login", data=case)
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_password_hashing(self, test_client, db_session):
        # Тест хеширования пароля
        user_data = UserCreate(email="security@test.com", password="S3cr3t!")
        response = test_client.post("/auth/register", json=user_data.dict())

        user = await db_session.execute(
            select(User).where(User.email == user_data.email)
        )
        db_user = user.scalar_one()

        assert db_user.hashed_password != user_data.password
        assert db_user.hashed_password.startswith("$2b$")

    async def test_jwt_token_validation(self, test_client, auth_headers):
        # Тест валидации JWT токена
        response = test_client.get("/users/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == "authuser@example.com"
