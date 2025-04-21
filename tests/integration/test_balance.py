import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_get_balance(test_client, auth_headers, test_balance):
    response = test_client.get("/balance/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["balance"] == 100.0

@pytest.mark.asyncio
async def test_topup_balance(test_client, auth_headers):
    response = test_client.post(
        "/balance/topup",
        headers=auth_headers,
        json={"amount": 50.0}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["balance"] == 50.0

@pytest.mark.asyncio
async def test_withdraw_balance(test_client, auth_headers, test_balance):
    response = test_client.post(
        "/balance/withdraw",
        headers=auth_headers,
        json={"amount": 30.0}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["balance"] == 70.0

@pytest.mark.asyncio
async def test_withdraw_insufficient_funds(test_client, auth_headers, test_balance):
    response = test_client.post(
        "/balance/withdraw",
        headers=auth_headers,
        json={"amount": 150.0}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "insufficient funds" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_withdraw_zero_balance(test_client, auth_headers):
    response = test_client.post(
        "/balance/withdraw",
        headers=auth_headers,
        json={"amount": 10.0}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "no balance record" in response.json()["detail"].lower()

@pytest.mark.parametrize("amount,expected_status", [
    (9999.99, 200),    # Верхний предел
    (-100.0, 422),     # Отрицательное значение
    (0.0, 422),        # Нулевое пополнение
    (100000.0, 422),   # Превышение лимита
    ("abc", 422)       # Нечисловое значение
])
def test_balance_topup_validation(test_client, auth_headers, amount, expected_status):
    response = test_client.post(
        "/balance/topup",
        headers=auth_headers,
        json={"amount": amount}
    )
    assert response.status_code == expected_status
