import pytest
from httpx import ASGITransport, AsyncClient
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app
from src.domain.models.user import CreateUser
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl

@pytest.fixture(scope="module")
async def client():
    """Create an async test client using FastAPI's ASGITransport."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.mark.anyio
async def test_get_users(client: AsyncClient, db_session: AsyncSession):
    """Test GET /user returns a list of users."""
    user_repo = UserRepositoryImpl(db_session)
    
    await user_repo.create_user(CreateUser(name="Robin", email="robin@example.com", password="pass123"))
    await user_repo.create_user(CreateUser(name="Luffy", email="luffy@example.com", password="pass123"))

    response = await client.get("/api/v1/user/")
    
    print(f"RESPONSE STATUS: {response.status_code}")
    print(f"RESPONSE BODY: {response.json()}")

    assert response.status_code == 200
    users = response.json()

    assert len(users) >= 2  
    assert any(user["email"] == "robin@example.com" for user in users)
    assert any(user["email"] == "luffy@example.com" for user in users)



@pytest.mark.anyio
async def test_get_user_by_id(client: AsyncClient, db_session: AsyncSession):
    """Test GET /user/{user_id} retrieves a specific user."""
    user_repo = UserRepositoryImpl(db_session)
    user = await user_repo.create_user(CreateUser(name="Dexter", email="dexter@example.com", password="pass123"))

    response = await client.get(f"/api/v1/user/{user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(user.id)
    assert data["name"] == "Dexter"
    assert data["email"] == "dexter@example.com"


@pytest.mark.anyio
async def test_get_user_by_id_not_found(client: AsyncClient):
    """Test GET /user/{user_id} returns 404 for non-existent user."""
    response = await client.get(f"/api/v1/user/{uuid4()}")

    assert response.status_code == 404


@pytest.mark.anyio
async def test_create_user(client: AsyncClient):
    """Test POST /api/v1/user successfully creates a user."""
    response = await client.post(
        "/api/v1/user/",
        json={
            "name": "Adam",
            "email": "adam@example.com",
            "password": "securepass",
            "is_active": True,
            "is_superuser": False
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Adam"


@pytest.mark.anyio
async def test_create_user_duplicate(client: AsyncClient, db_session: AsyncSession):
    """Test POST /user returns 400 for duplicate users."""
    user_repo = UserRepositoryImpl(db_session)
    await user_repo.create_user(CreateUser(name="Bruce", email="bruce@example.com", password="pass123"))

    response = await client.post(
        "/api/v1/user/",
        json={"name": "Bruce", "email": "bruce@example.com", "password": "pass123"}
    )

    assert response.status_code == 400
