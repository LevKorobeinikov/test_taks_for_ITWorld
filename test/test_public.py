import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_public_endpoints():
    async with AsyncClient(app=app, base_url="http://test") as client:
        r = await client.get("/api/v1/posts")
        assert r.status_code == 200
        r = await client.get("/api/v1/categories")
        assert r.status_code == 200


