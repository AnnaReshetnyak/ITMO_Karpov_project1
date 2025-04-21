import pytest
from fastapi import status
from lesson_2.app.models import User, Transaction
from lesson_2.app.schemas import UserCreate, Token


class TestUserWithBalanceFlow:
    """Тестирование полного цикла работы пользователя с балансом"""

    @pytest.mark.asyncio
    async def test_full_user_flow(self, client, db_session):
        """
        1. Регистрация нового пользователя
        2. Авторизация
        3. Проверка начального баланса
        4. Пополнение баланса
        5. Проверка обновленного баланса
        6. Проверка истории транзакций
        """

        # Шаг 1: Регистрация
        user_data = {
            "email": "test.user@example.com",
            "password": "SecurePass123!",
            "confirm_password": "SecurePass123!"
        }
        reg_response = await client.post("/auth/register", json=user_data)
        assert reg_response.status_code == status.HTTP_201_CREATED

        # Шаг 2: Авторизация
        auth_data = {
            "username": "test.user@example.com",
            "password": "SecurePass123!"
        }
        auth_response = await client.post("/auth/jwt/login", data=auth_data)
        assert auth_response.status_code == status.HTTP_200_OK

        tokens = auth_response.json()
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}

        # Шаг 3: Проверка начального баланса
        balance_response = await client.get("/balance", headers=headers)
        assert balance_response.status_code == status.HTTP_200_OK
        assert balance_response.json()["balance"] == 0.0

        # Шаг 4: Пополнение баланса
        topup_data = {"amount": 1500.0}
        topup_response = await client.post(
            "/balance/topup",
            json=topup_data,
            headers=headers
        )
        assert topup_response.status_code == status.HTTP_200_OK
        assert topup_response.json()["balance"] == 1500.0

        # Шаг 5: Проверка обновленного баланса
        updated_balance_response = await client.get("/balance", headers=headers)
        assert updated_balance_response.json()["balance"] == 1500.0

        # Шаг 6: Проверка истории транзакций
        transactions_response = await client.get(
            "/transactions",
            headers=headers
        )
        assert transactions_response.status_code == status.HTTP_200_OK
        transactions = transactions_response.json()

        assert len(transactions) == 1
        assert transactions[0]["amount"] == 1500.0
        assert transactions[0]["type"] == "DEPOSIT"
