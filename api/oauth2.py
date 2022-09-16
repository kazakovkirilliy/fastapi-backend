from random import randint
from typing import Optional
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from . import settings

from .schemas import token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/oauth/login"
)


# SECRET
# Algorithm
# Expiration time

SECRET_KEY = str(settings.SECRET_KEY)
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(access_token: str, credentials_exception):
    try:
        payload = jwt.decode(token=access_token,
                             key=SECRET_KEY, algorithms=ALGORITHM)

        user_id: str = payload.get("user_id")

        if not user_id:
            raise credentials_exception

        token_data = token.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(access_token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(access_token=access_token, credentials_exception=credentials_exception)
