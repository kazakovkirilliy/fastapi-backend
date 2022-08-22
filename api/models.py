from uuid import uuid4

from geoalchemy2 import Geography
from sqlalchemy import (FLOAT, TIMESTAMP, Column, Float, ForeignKey, String,
                        text)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from api.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    location = relationship("PostLocation", uselist=False)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Like(Base):
    __tablename__ = "likes"

    post_id = Column(UUID(as_uuid=True), ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)


class Participation(Base):
    __tablename__ = "participations"

    post_id = Column(UUID(as_uuid=True), ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)


class PostLocation(Base):
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey(
        "posts.id", ondelete="CASCADE"))

    country = Column(String)
    city = Column(String)
    street = Column(String)
    house_number = Column(String)

    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    geography = Column(
        Geography(srid=4326, geometry_type="POINT"), index=True)
