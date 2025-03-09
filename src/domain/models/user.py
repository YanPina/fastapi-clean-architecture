from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):  # type: ignore
    id: Optional[UUID] = Field(default_factory=uuid4)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class User(BaseUser):
    name: str
    email: EmailStr


class CreateUser(User):
    password: str
