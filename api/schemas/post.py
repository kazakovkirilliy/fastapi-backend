from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from api.schemas.user import UserResponse


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    title: str | None
    content: str | None


class Post(PostBase):
    id: UUID
    created_at: datetime
    owner_id: UUID

    class Config:
        orm_mode = True


class PostWithOwner(PostBase):
    id: UUID
    created_at: datetime
    owner_id: UUID
    owner: UserResponse

    class Config:
        orm_mode = True
