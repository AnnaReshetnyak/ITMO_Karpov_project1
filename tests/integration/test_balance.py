from fastapi.testclient import TestClient
from lesson_2.main import app
from lesson_2.app.database.database import init_db
import pytest

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def initialize_db():
    init_db()


def test_balance_workflow():
    # Регистрация пользователя
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "string"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Проверка баланса
    response = client.get(
        "/balance/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 0.0

    # Пополнение баланса
    response = client.post(
        "/balance/topup",
        headers={"Authorization": f"Bearer {token}"},
        json={"amount": 100.0}
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 100.0
