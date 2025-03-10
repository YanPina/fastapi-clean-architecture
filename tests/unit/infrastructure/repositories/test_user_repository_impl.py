import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.domain.models.user import CreateUser
from src.core.exceptions import DuplicatedError, NotFoundError, ValidationError
from sqlalchemy.exc import SQLAlchemyError

@pytest.mark.asyncio
async def test_create_user_success(db_session: AsyncSession):
    """Test successfully creating a user."""
    user_repo = UserRepositoryImpl(db_session)
    
    user_data = CreateUser(name="Charlie", email="charlie@example.com", password="plaintextpass")
    
    user = await user_repo.create_user(user_data)

    assert user.name == "Charlie"
    assert user.email == "charlie@example.com"

@pytest.mark.asyncio
async def test_create_duplicate_user(db_session: AsyncSession):
    """Test that creating a duplicate user raises DuplicatedError."""
    user_repo = UserRepositoryImpl(db_session)

    user_data = CreateUser(name="Alice", email="alice@example.com", password="password123")
    await user_repo.create_user(user_data)

    with pytest.raises(DuplicatedError):
        await user_repo.create_user(user_data)


@pytest.mark.asyncio
async def test_get_user_by_id(db_session: AsyncSession, mocker):
    """Test retrieving a user by ID."""
    user_repo = UserRepositoryImpl(db_session)

    user_data = CreateUser(name="Bob", email="bob@example.com", password="securepass")
    user = await user_repo.create_user(user_data)

    retrieved_user = await user_repo.get_user_by_id(user.id)

    assert retrieved_user.id == user.id
    assert retrieved_user.name == "Bob"
    assert retrieved_user.email == "bob@example.com"

    mocker.patch.object(db_session, "get", side_effect=SQLAlchemyError("DB failure"))

    with pytest.raises(NotFoundError, match="DB failure"):
        await user_repo.get_user_by_id(user.id)


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(db_session: AsyncSession):
    """Test that retrieving a non-existent user raises NotFoundError."""
    user_repo = UserRepositoryImpl(db_session)

    with pytest.raises(NotFoundError):
        await user_repo.get_user_by_id(uuid4())


@pytest.mark.asyncio
async def test_get_all_users(db_session: AsyncSession):
    """Test retrieving all users."""
    user_repo = UserRepositoryImpl(db_session)

    await user_repo.create_user(CreateUser(name="John", email="john@example.com", password="pass1"))
    await user_repo.create_user(CreateUser(name="Doe", email="doe@example.com", password="pass2"))

    users = await user_repo.get_all_users()

    assert len(users) >= 2
    assert any(user.email == "john@example.com" for user in users)
    assert any(user.email == "doe@example.com" for user in users)


@pytest.mark.asyncio
async def test_delete_user_success(db_session: AsyncSession):
    """Test successfully deleting a user."""
    user_repo = UserRepositoryImpl(db_session)

    user = await user_repo.create_user(CreateUser(name="Eve", email="eve@example.com", password="mypassword"))

    response = await user_repo.delete_user(user.id)

    assert response == {"message": "User deleted"}

    with pytest.raises(NotFoundError):
        await user_repo.get_user_by_id(user.id)


@pytest.mark.asyncio
async def test_delete_user_not_found(db_session: AsyncSession):
    """Test that deleting a non-existent user raises NotFoundError."""
    user_repo = UserRepositoryImpl(db_session)

    with pytest.raises(NotFoundError):
        await user_repo.delete_user(uuid4())


@pytest.mark.asyncio
async def test_create_user_db_error(db_session: AsyncSession, mocker):
    """Test that a database error during user creation raises ValidationError."""
    user_repo = UserRepositoryImpl(db_session)

    # Mock the session.commit() to throw an exception
    mocker.patch.object(db_session, "commit", side_effect=SQLAlchemyError("DB error"))

    user_data = CreateUser(name="Bruno", email="bruno@example.com", password="plaintextpass")

    with pytest.raises(ValidationError):
        await user_repo.create_user(user_data)


@pytest.mark.asyncio
async def test_delete_user_db_error(db_session: AsyncSession, mocker):
    """Test that a database error during deletion raises ValidationError."""
    user_repo = UserRepositoryImpl(db_session)

    user = await user_repo.create_user(CreateUser(name="Eve", email="eve@example.com", password="mypassword"))

    # Mock the session.commit() to throw an exception
    mocker.patch.object(db_session, "commit", side_effect=SQLAlchemyError("DB error"))

    with pytest.raises(ValidationError):
        await user_repo.delete_user(user.id)
