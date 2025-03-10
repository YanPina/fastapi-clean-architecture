import pytest
from uuid import uuid4, UUID
from typing import Dict, List
from src.domain.models.user import CreateUser, User
from src.domain.repositories.user_repository import UserRepository


class TestUserRepository(UserRepository):
    """Concrete class for testing UserRepository abstract methods."""
    
    async def get_all_users(self) -> List[User]:
        return [User(id=uuid4(), name="Test User", email="test@example.com")]

    async def get_user_by_id(self, user_id: UUID) -> User:
        return User(id=user_id, name="Found User", email="found@example.com")

    async def create_user(self, user: CreateUser) -> User:
        return User(id=uuid4(), name=user.name, email=user.email)

    async def delete_user(self, user_id: UUID) -> Dict[str, str]:
        return {"message": f"User {user_id} deleted"}


@pytest.mark.asyncio
async def test_user_repository_methods():
    """Test all abstract methods in UserRepository using a concrete implementation."""
    repo = TestUserRepository()

    users = await repo.get_all_users()
    assert len(users) == 1
    assert users[0].name == "Test User"

    user = await repo.get_user_by_id(uuid4())
    assert user.name == "Found User"

    new_user = await repo.create_user(CreateUser(name="MockUser", email="mock@example.com", password="password"))
    assert new_user.name == "MockUser"

    response = await repo.delete_user(uuid4())
    assert "deleted" in response["message"]


def test_user_repository_cannot_be_instantiated():
    """Ensure UserRepository cannot be instantiated directly."""
    with pytest.raises(TypeError):
        UserRepository()
