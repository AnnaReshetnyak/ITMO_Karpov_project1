from locust import HttpUser, task, between


class PredictionLoadTest(HttpUser):
    wait_time = between(1, 3)
    host = "http://app:8000"

    @task
    def test_high_load(self):
        # Аутентификация
        auth = self.client.post("/auth/login", json={
            "username": "load_user@test.com",
            "password": "load_password"
        })
        token = auth.json()["access_token"]

        # Параллельные запросы
        self.client.post(
            "/predict",
            headers={"Authorization": f"Bearer {token}"},
            json={"input_data": {"param": 0.5}}
        )
