from typing import Dict, List
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.exceptions import DuplicatedError, NotFoundError, ValidationError
from src.domain.models.user import CreateUser, User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models.user import User as UserEntity
from src.infrastructure.security.hash import hash_password


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_users(self) -> List[User]:
        result = await self.session.execute(select(UserEntity))
        users = result.scalars().all()
        return [self.__to_domain(user) for user in users]

    async def get_user_by_id(self, user_id: UUID) -> User:
        try:
            user = await self.session.get(UserEntity, user_id)
            if user is None:
                raise NotFoundError(f"User with ID {user_id} not found.")

            return self.__to_domain(user)
        except SQLAlchemyError as error:
            raise NotFoundError(str(error))

    async def __is_user_exist(self, user_email: UUID) -> bool:
        statement = select(UserEntity.id).where(UserEntity.email == user_email)
        result = await self.session.execute(statement)
        return result.scalar() is not None

    async def create_user(self, user: CreateUser) -> User:
        if await self.__is_user_exist(user.email):
            raise DuplicatedError(f"User {user.email} already exist")

        try:
            user_data = user.model_dump(
                exclude={"id", "created_at", "updated_at"}
            )
            user_data["password"] = hash_password(user_data.pop("password"))

            user_db = UserEntity(**user_data)
            self.session.add(user_db)
            await self.session.commit()
            await self.session.refresh(user_db)
            return self.__to_domain(user_db)
        except SQLAlchemyError as error:
            raise ValidationError(str(error))

    async def delete_user(self, user_id: UUID) -> Dict[str, str]:
        try:
            stmt = select(UserEntity).where(UserEntity.id == user_id)

            result = await self.session.execute(stmt)
            user = result.scalars().first()

            if not user:
                raise NotFoundError(f"User with ID {user_id} not found.")

            await self.session.delete(user)
            await self.session.commit()
            return {"message": "User deleted"}

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ValidationError(
                f"Database error while deleting user ID {user_id}: {e}"
            )

    def __to_domain(self, user: UserEntity) -> User:
        return User(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
