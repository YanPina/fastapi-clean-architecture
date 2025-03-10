from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from src.core.dependencies import get_user_controller
from src.domain.models.user import CreateUser, User
from src.interfaces.controllers.user_controller import UserController

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/", response_model=List[User])
async def get_users(
    controller: UserController = Depends(get_user_controller),
) -> List[User]:
    return await controller.get_users()


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: UUID, controller: UserController = Depends(get_user_controller)
) -> User:
    return await controller.get_user(user_id)


@router.post("/", response_model=User)
async def create_user(
    user: CreateUser, controller: UserController = Depends(get_user_controller)
) -> User:
    return await controller.create_user(user)
