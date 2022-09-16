from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, status, HTTPException, Form
from pydantic import ValidationError
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from api import oauth2
from api.settings import SECRET_KEY

from ..database import get_db

from .. import utils, models

from ..schemas.token import Token

router = APIRouter(prefix="/oauth", tags=["auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 2 * 365 # 2 years


class OAuth2PasswordRefreshRequestForm:
    def __init__(
        self,
        grant_type: str = Form(None, regex="password|refresh_token"),
        username: Optional[str] = Form(""),
        password: Optional[str] = Form(""),
        refresh_token: Optional[str] = Form(""),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.refresh_token = refresh_token


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRefreshRequestForm = Depends(), db: Session = Depends(get_db)):
    print(form_data.username)
    print(form_data.password)
    if form_data.grant_type == "password":
        user = authenticate_user(form_data.username, form_data.password, db)
    else:
        user = refresh_user(form_data.refresh_token, db)
    if not user:
        print("getting token...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return get_access_token(user, form_data.grant_type == "password")


def get_access_token(user: models.User, include_refresh: bool):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"user_id": user.id}

    access_token = oauth2.create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    response_data: Token = Token(
        access_token=access_token,
        at_exp_time=int(access_token_expires.total_seconds()),
    )

    if include_refresh:
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        refresh_token = oauth2.create_access_token(
            data=token_data, expires_delta=refresh_token_expires
        )
        response_data.rt_exp_time = int(refresh_token_expires.total_seconds())
        response_data.refresh_token = refresh_token

    print(response_data)

    return response_data


def authenticate_user(username: str, password: str, db: Session) -> models.User:
    user: models.User = db.query(models.User).filter(
        models.User.username == username).first()

    if not user or user.password is None:
        return None
    if not utils.verify_password(password, user.password):
        return None

    return user


def refresh_user(refresh_token: str, db: Session) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token validation error",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            refresh_token,
            str(SECRET_KEY),
            algorithms=[oauth2.ALGORITHM],
        )

        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

    except (JWTError, ValidationError) as jwte:
        raise credentials_exception from jwte

    user: models.User = db.query(models.User).filter(
        models.User.id == user_id).first()

    if user is None:
        raise credentials_exception
    return user
