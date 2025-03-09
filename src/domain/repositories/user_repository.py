from abc import ABC, abstractmethod
from typing import Dict, List
from uuid import UUID

from src.domain.models.user import CreateUser, User


class UserRepository(ABC):
    @abstractmethod
    async def get_all_users(self) -> List[User]:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> User:
        ...

    @abstractmethod
    async def create_user(self, user: CreateUser) -> User:
        ...

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> Dict[str, str]:
        ...
