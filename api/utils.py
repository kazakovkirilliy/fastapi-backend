from json import JSONEncoder
from uuid import UUID
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash(string: str):
    return pwd_context.hash(string)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


old_default = JSONEncoder.default


# https://github.com/jazzband/django-push-notifications/issues/586
def new_default(self, obj):
    if isinstance(obj, UUID):
        return str(obj)
    return old_default(self, obj)


JSONEncoder.default = new_default
