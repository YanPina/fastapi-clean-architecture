from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.user_use_case import UserUseCase
from src.infrastructure.database.base import get_db
from src.infrastructure.repositories.user_repository_impl import (
    UserRepositoryImpl,
)
from src.interfaces.controllers.user_controller import UserController


def get_user_respository(
    session: AsyncSession = Depends(get_db),
) -> UserRepositoryImpl:
    return UserRepositoryImpl(session)


def get_user_use_case(
    repository: UserRepositoryImpl = Depends(get_user_respository),
) -> UserUseCase:
    return UserUseCase(repository)


def get_user_controller(
    use_case: UserUseCase = Depends(get_user_use_case),
) -> UserController:
    return UserController(use_case)
