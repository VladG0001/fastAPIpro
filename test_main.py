import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_home():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.text == "Welcome to the Web Scraper API! Use /parse endpoint to parse URLs."

@pytest.mark.asyncio
async def test_parse_titles():
    test_url = "https://example.com"
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(f"/parse?url={test_url}&extract=titles")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_parse_links():
    test_url = "https://example.com"
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(f"/parse?url={test_url}&extract=links")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_invalid_url():
    invalid_url = "invalid-url"
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(f"/parse?url={invalid_url}&extract=titles")
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_invalid_extract_param():
    test_url = "https://example.com"
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get(f"/parse?url={test_url}&extract=invalid")
    assert response.status_code == 400
