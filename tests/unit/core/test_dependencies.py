import pytest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.dependencies import (
    get_user_respository,
    get_user_use_case,
    get_user_controller,
)
from src.application.use_cases.user_use_case import UserUseCase
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.interfaces.controllers.user_controller import UserController


@pytest.fixture
def mock_session():
    """Mock AsyncSession for database."""
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_user_repository(mock_session):
    """Mock UserRepositoryImpl using a fake session."""
    mock_repo = MagicMock(spec=UserRepositoryImpl)
    mock_repo.session = mock_session
    return mock_repo


@pytest.fixture
def mock_user_use_case(mock_user_repository):
    """Mock UserUseCase with a fake repository."""
    mock_use_case = MagicMock(spec=UserUseCase)
    mock_use_case.user_repository = mock_user_repository
    return mock_use_case


@pytest.fixture
def mock_user_controller(mock_user_use_case):
    """Mock UserController with a fake use case."""
    mock_controller = MagicMock(spec=UserController)
    mock_controller.user_use_case = mock_user_use_case
    return mock_controller


def test_get_user_respository(mock_session):
    """Test the user repository dependency injection."""
    repository = get_user_respository(session=mock_session)
    assert isinstance(repository, UserRepositoryImpl)
    assert repository.session == mock_session


def test_get_user_use_case(mock_user_repository):
    """Test the user use case dependency injection."""
    use_case = get_user_use_case(repository=mock_user_repository)
    assert isinstance(use_case, UserUseCase)
    assert use_case.user_repository == mock_user_repository


def test_get_user_controller(mock_user_use_case):
    """Test the user controller dependency injection."""
    controller = get_user_controller(use_case=mock_user_use_case)
    assert isinstance(controller, UserController)
    assert controller.user_use_case == mock_user_use_case
