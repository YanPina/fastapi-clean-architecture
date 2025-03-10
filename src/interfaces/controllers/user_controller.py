from typing import Dict, List
from uuid import UUID

from src.application.use_cases.user_use_case import UserUseCase
from src.domain.models.user import CreateUser, User


class UserController:
    def __init__(self, user_use_case: UserUseCase) -> None:
        self.user_use_case = user_use_case

    async def get_users(self) -> List[User]:
        return await self.user_use_case.list_users()

    async def get_user(self, user_id: UUID) -> User:
        return await self.user_use_case.get_user(user_id)

    async def create_user(self, user_data: CreateUser) -> User:
        return await self.user_use_case.register_user(user_data)

    async def delete_user(self, user_id: UUID) -> Dict[str, str]:
        return await self.user_use_case.delete_user(user_id)
