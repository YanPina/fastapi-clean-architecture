import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from uuid import uuid4
from src.application.use_cases.user_use_case import UserUseCase
from src.domain.models.user import CreateUser, User
from src.domain.repositories.user_repository import UserRepository


@pytest_asyncio.fixture
async def user_repo_mock():
    """Mock the UserRepository dependency."""
    mock_repo = AsyncMock(spec=UserRepository)
    return mock_repo


@pytest_asyncio.fixture
async def user_use_case(user_repo_mock):
    """Inject the mocked UserRepository into UserUseCase."""
    return UserUseCase(user_repo_mock)


@pytest.mark.asyncio
async def test_list_users(user_use_case, user_repo_mock):
    """Test that list_users() returns a list of users."""
    user_repo_mock.get_all_users.return_value = [
        User(id=uuid4(), name="Alice", email="alice@example.com"),
        User(id=uuid4(), name="Bob", email="bob@example.com"),
    ]

    users = await user_use_case.list_users()

    assert len(users) == 2
    assert users[0].name == "Alice"
    assert users[1].name == "Bob"
    user_repo_mock.get_all_users.assert_called_once()


@pytest.mark.asyncio
async def test_get_user(user_use_case, user_repo_mock):
    """Test that get_user() returns a user by ID."""
    user_id = uuid4()
    user_repo_mock.get_user_by_id.return_value = User(
        id=user_id, name="Alice", email="alice@example.com"
    )

    user = await user_use_case.get_user(user_id)

    assert user.id == user_id
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    user_repo_mock.get_user_by_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_register_user(user_use_case, user_repo_mock):
    """Test that register_user() creates and returns a new user."""
    new_user = CreateUser(name="Charlie", email="charlie@example.com", password="hashedpass")
    created_user = User(id=uuid4(), name="Charlie", email="charlie@example.com")

    user_repo_mock.create_user.return_value = created_user

    user = await user_use_case.register_user(new_user)

    assert user.name == "Charlie"
    assert user.email == "charlie@example.com"
    user_repo_mock.create_user.assert_called_once_with(new_user)


@pytest.mark.asyncio
async def test_delete_user(user_use_case, user_repo_mock):
    """Test that delete_user() successfully removes a user."""
    user_id = uuid4()
    user_repo_mock.delete_user.return_value = {"message": "User deleted"}

    response = await user_use_case.delete_user(user_id)

    assert response == {"message": "User deleted"}
    user_repo_mock.delete_user.assert_called_once_with(user_id)
