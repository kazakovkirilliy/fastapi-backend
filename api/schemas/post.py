from datetime import datetime
from typing import Any, Optional
from uuid import UUID
from api.schemas.location import LocationResponse
from api.schemas.user import UserResponse
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostUpdate(PostBase):
    title: str | None
    content: str | None


class Post(PostBase):
    id: UUID
    created_at: datetime
    owner_id: UUID

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    longitude: float
    latitude: float


class PostWithOwner(PostBase):
    id: UUID
    created_at: datetime
    owner_id: UUID
    location: Optional[LocationResponse]

    class Config:
        orm_mode = True
