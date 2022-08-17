"""
Main User API.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import PlainTextResponse, JSONResponse

from api.models import User
from api.routers.common import RequestPager, ResponsePager
from .. import utils
from api import oauth2

from ..schemas import user, token

from ..database import get_db


from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["users"])


# @router.get("")
# def user_get_all(paging: RequestPager = Depends(), db: Session = Depends(get_db)):

#     content = db.query(User).offset(paging.offset).limit(paging.limit).all()
#     total_count = db.query(User).count()

#     return ResponsePager(
#         content=content,
#         count=len(content),
#         limit=paging.limit,
#         offset=paging.offset,
#         order=paging.order,
#         order_by=paging.order_by,
#         total_count=total_count,
#     )


@router.get("/{username}", response_model=user.UserResponse, response_class=JSONResponse)
def user_get_one(username: str, db: Session = Depends(get_db)):
    """
    Read specific user.
    """
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with name: {username} was not found")

    return user


@router.post("", status_code=status.HTTP_201_CREATED, response_model=token.Token)
def user_create_one(user: user.UserCreate, db: Session = Depends(get_db)):

    if (len(user.username) < 4):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Username must be at least 4 letters long")
    elif (not user.username.isalnum()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Username must contain only characters and numbers")
    elif (len(user.password) < 5):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Password must be at least 5 letters long")
    elif (user.password == "12345" or user.password == "abcde" or user.password == "password" or user.password == user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Provided password is weak")

    # hash password
    hashed_password = utils.hash(string=user.password)
    user.password = hashed_password

    try:
        new_user = User(**user.dict())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = oauth2.create_access_token(
            data={"user_id": new_user.id})

        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User already exists")


@router.put("/{user_id}")
def user_update_one(user_id: str, updated_user: user.UserUpdate, db: Session = Depends(get_db)):
    """
    Update existing user
    """
    user_query = db.query(User).filter(User.id == user_id)

    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {user_id} does not exist")

    user_query.update(updated_user.dict(exclude_unset=True),
                      synchronize_session=False)

    db.commit()

    return user_query.first()


# @router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# def user_delete_one(user_id: str, db: Session = Depends(get_db)):
#     """
#     Delete user
#     """
#     user_query = db.query(User).filter(User.id == user_id)

#     if user_query.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with id: {user_id} was not found")

#     user_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)
