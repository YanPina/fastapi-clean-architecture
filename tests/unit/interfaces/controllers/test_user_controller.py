import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from src.interfaces.controllers.user_controller import UserController
from src.application.use_cases.user_use_case import UserUseCase
from src.domain.models.user import CreateUser, User


@pytest.fixture
def mock_user_use_case():
    """Mock UserUseCase for UserController tests."""
    return AsyncMock(spec=UserUseCase)


@pytest.fixture
def user_controller(mock_user_use_case):
    """Create UserController instance with mocked UserUseCase."""
    return UserController(mock_user_use_case)


@pytest.mark.asyncio
async def test_get_users(user_controller: UserController, mock_user_use_case):
    """Test get_users method in UserController."""
    mock_user_use_case.list_users.return_value = [
        User(id=uuid4(), name="Alice", email="alice@example.com"),
        User(id=uuid4(), name="Bob", email="bob@example.com"),
    ]

    response = await user_controller.get_users()

    assert len(response) == 2
    assert response[0].name == "Alice"
    assert response[1].name == "Bob"
    mock_user_use_case.list_users.assert_called_once()


@pytest.mark.asyncio
async def test_get_user(user_controller: UserController, mock_user_use_case):
    """Test get_user method in UserController."""
    user_id = uuid4()
    mock_user_use_case.get_user.return_value = User(id=user_id, name="Charlie", email="charlie@example.com")

    response = await user_controller.get_user(user_id)

    assert response.id == user_id
    assert response.name == "Charlie"
    assert response.email == "charlie@example.com"
    mock_user_use_case.get_user.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_create_user(user_controller: UserController, mock_user_use_case):
    """Test create_user method in UserController."""
    user_data = CreateUser(name="David", email="david@example.com", password="securepass")
    mock_user_use_case.register_user.return_value = User(id=uuid4(), name="David", email="david@example.com")

    response = await user_controller.create_user(user_data)

    assert response.name == "David"
    assert response.email == "david@example.com"
    mock_user_use_case.register_user.assert_called_once_with(user_data)


@pytest.mark.asyncio
async def test_delete_user(user_controller: UserController, mock_user_use_case):
    """Test delete_user method in UserController."""
    user_id = uuid4()
    mock_user_use_case.delete_user.return_value = {"message": "User deleted"}

    response = await user_controller.delete_user(user_id)

    assert response == {"message": "User deleted"}
    mock_user_use_case.delete_user.assert_called_once_with(user_id)
