import pytest
from httpx import ASGITransport, AsyncClient
from src.main import app

@pytest.mark.anyio
async def test_app_starts():
    """Ensure the FastAPI app starts correctly and the root endpoint is reachable."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    assert response.text == '"service is working"'

def test_router_included():
    """Ensure API router is properly included."""
    routes = [route.path for route in app.router.routes]
    
    assert "/api/v1/user/" in routes
