import pytest
from locust import HttpUser, task, between


class PredictionLoadTest(HttpUser):
    wait_time = between(1, 3)

    @task
    def test_prediction_load(self):
        auth = self.client.post("/auth/login", json={
            "username": "demo@example.com",
            "password": "demo"
        })
        token = auth.json()["access_token"]

        self.client.post(
            "/predict",
            headers={"Authorization": f"Bearer {token}"},
            json={"input_data": {"feature1": 0.5, "feature2": 1.2}}
        )
