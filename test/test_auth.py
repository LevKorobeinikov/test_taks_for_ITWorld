import pytest
from httpx import AsyncClient
from fastapi import status

from app.main import app


@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # register
        r = await client.post("/api/v1/auth/register", json={"email": "u1@example.com", "password": "pass12345"})
        assert r.status_code == status.HTTP_200_OK
        # login
        r = await client.post(
            "/api/v1/auth/login",
            data={"username": "u1@example.com", "password": "pass12345"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert r.status_code == status.HTTP_200_OK
        body = r.json()
        assert "access_token" in body and "refresh_token" in body


