import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_user_registration(test_client):
    response = test_client.post(
        "/auth/register",
        json={
            "email": "new.user@example.com",
            "password": "securepassword123"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_duplicate_registration(test_client, test_user):
    response = test_client.post(
        "/auth/register",
        json={
            "email": test_user.email,
            "password": "anypassword"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.asyncio
async def test_user_login(test_client, auth_headers):
    response = test_client.post(
        "/auth/login",
        data={
            "username": "authuser@example.com",
            "password": "password"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_get_current_user(test_client, auth_headers):
    response = test_client.get(
        "/users/me",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "authuser@example.com"
