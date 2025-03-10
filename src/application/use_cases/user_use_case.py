from typing import Dict, List
from uuid import UUID

from src.domain.models.user import CreateUser, User
from src.domain.repositories.user_repository import UserRepository


class UserUseCase:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def list_users(self) -> List[User]:
        return await self.user_repository.get_all_users()

    async def get_user(self, user_id: UUID) -> User:
        return await self.user_repository.get_user_by_id(user_id)

    async def register_user(self, user: CreateUser) -> User:
        return await self.user_repository.create_user(user)

    async def delete_user(self, user_id: UUID) -> Dict[str, str]:
        return await self.user_repository.delete_user(user_id)
