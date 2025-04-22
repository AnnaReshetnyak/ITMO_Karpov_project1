import pytest
from fastapi.testclient import TestClient
from lesson_2.main import app
from unittest.mock import AsyncMock, patch


client = TestClient(app)



def test_prediction_flow():
    # Регистрация
    client.post("/auth/register", json={
        "email": "mluser@example.com",
        "password": "mlpassword"
    })

    # Логин
    login = client.post("/auth/login", data={
        "username": "mluser@example.com",
        "password": "mlpassword"
    })
    token = login.json()["access_token"]

    # Пополнение баланса
    client.post("/balance/topup",
                headers={"Authorization": f"Bearer {token}"},
                json={"amount": 100}
                )

    # Создание предсказания
    prediction = client.post(
        "/predict",
        headers={"Authorization": f"Bearer {token}"},
        json={"input_data": {"param1": 1.2, "param2": 0.8}}
    )

    assert prediction.status_code == 200
    assert "task_id" in prediction.json()

async def test_prediction_flow_with_mocked_rabbitmq(test_client, auth_headers):
    with patch("app.rabbitmq.producer.send_prediction_task", new=AsyncMock()) as mock_send:
        response = test_client.post(
            "/predict",
            headers=auth_headers,
            json={"input_data": {"param1": 1.2}}
        )
        mock_send.assert_awaited_once()
        assert response.json()["status"] == "pending"
